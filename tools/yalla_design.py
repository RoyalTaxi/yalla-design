#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
TOKENS_DIR = ROOT / "tokens"

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
RESOURCE_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
THEMED_IMAGE_NAME = re.compile(r"^[A-Z][A-Za-z0-9]*$")


class DesignError(ValueError):
    pass


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DesignError(f"{path.relative_to(ROOT)} is not valid JSON: {exc}") from exc


def load_tokens(root: Path = ROOT) -> dict:
    tokens_dir = root / "tokens"
    return {
        "colors": load_json(tokens_dir / "colors.json"),
        "typography": load_json(tokens_dir / "typography.json"),
        "themedImages": load_json(tokens_dir / "themed-images.json"),
    }


def require_dict(value: object, label: str) -> dict:
    if not isinstance(value, dict):
        raise DesignError(f"{label} must be an object")
    return value


def require_list(value: object, label: str) -> list:
    if not isinstance(value, list):
        raise DesignError(f"{label} must be an array")
    return value


def validate_hex(value: object, label: str) -> None:
    if not isinstance(value, str) or not HEX_COLOR.match(value):
        raise DesignError(f"{label} must be a #RRGGBB color")


def validate_colors(colors: dict) -> None:
    schemes = require_dict(colors.get("schemes"), "colors.schemes")
    if set(schemes) != {"light", "dark"}:
        raise DesignError("colors.schemes must contain exactly light and dark")

    light = require_dict(schemes["light"], "colors.schemes.light")
    dark = require_dict(schemes["dark"], "colors.schemes.dark")
    if light.keys() != dark.keys():
        raise DesignError("light and dark color groups must have the same shape")

    for group_name, light_group_value in light.items():
        light_group = require_dict(light_group_value, f"colors.schemes.light.{group_name}")
        dark_group = require_dict(dark[group_name], f"colors.schemes.dark.{group_name}")
        if light_group.keys() != dark_group.keys():
            raise DesignError(f"light and dark color group '{group_name}' must have the same keys")
        for token_name, color in light_group.items():
            validate_hex(color, f"colors.schemes.light.{group_name}.{token_name}")
            validate_hex(dark_group[token_name], f"colors.schemes.dark.{group_name}.{token_name}")

    accent = require_dict(colors.get("accent"), "colors.accent")
    for token_name, color in accent.items():
        validate_hex(color, f"colors.accent.{token_name}")

    gradients = require_dict(colors.get("gradients"), "colors.gradients")
    for gradient_name, stops_value in gradients.items():
        stops = require_list(stops_value, f"colors.gradients.{gradient_name}")
        if len(stops) < 2:
            raise DesignError(f"colors.gradients.{gradient_name} must have at least two stops")
        previous_position = -1.0
        for index, stop_value in enumerate(stops):
            stop = require_dict(stop_value, f"colors.gradients.{gradient_name}[{index}]")
            validate_hex(stop.get("color"), f"colors.gradients.{gradient_name}[{index}].color")
            position = stop.get("position")
            if not isinstance(position, (int, float)) or position < 0 or position > 1:
                raise DesignError(f"colors.gradients.{gradient_name}[{index}].position must be between 0 and 1")
            if position < previous_position:
                raise DesignError(f"colors.gradients.{gradient_name} positions must be sorted")
            previous_position = float(position)


def validate_typography(typography: dict) -> None:
    font_resources = require_dict(typography.get("fontResources"), "typography.fontResources")
    required_platforms = {"android", "ios", "cmpAndroid", "cmpIos"}
    if set(font_resources) != required_platforms:
        raise DesignError(f"typography.fontResources must contain {sorted(required_platforms)}")

    required_roles = {"normal", "medium", "bold", "carNumber"}
    for platform, resources_value in font_resources.items():
        resources = require_dict(resources_value, f"typography.fontResources.{platform}")
        if set(resources) != required_roles:
            raise DesignError(f"typography.fontResources.{platform} must contain {sorted(required_roles)}")
        for role, resource_name in resources.items():
            if not isinstance(resource_name, str) or not RESOURCE_NAME.match(resource_name):
                raise DesignError(f"typography.fontResources.{platform}.{role} must be a resource name")

    styles = require_dict(typography.get("styles"), "typography.styles")
    if not styles:
        raise DesignError("typography.styles must not be empty")
    required_styles = {
        "title.xLarge",
        "title.large",
        "title.base",
        "body.caption",
        "body.large.regular",
        "body.large.medium",
        "body.large.bold",
        "body.base.regular",
        "body.base.medium",
        "body.base.bold",
        "body.small.regular",
        "body.small.medium",
        "body.small.bold",
        "custom.carNumber",
    }
    missing_styles = sorted(required_styles - set(styles))
    if missing_styles:
        raise DesignError(f"typography.styles is missing required styles: {missing_styles}")
    for style_name, style_value in styles.items():
        style = require_dict(style_value, f"typography.styles.{style_name}")
        font = style.get("font")
        if font not in required_roles:
            raise DesignError(f"typography.styles.{style_name}.font must be one of {sorted(required_roles)}")
        for metric in ("sizeSp", "lineHeightSp"):
            value = style.get(metric)
            if not isinstance(value, (int, float)) or value <= 0:
                raise DesignError(f"typography.styles.{style_name}.{metric} must be a positive number")


def validate_themed_images(themed_images: dict) -> None:
    images = require_list(themed_images.get("images"), "themedImages.images")
    seen_names: set[str] = set()
    for index, image_value in enumerate(images):
        image = require_dict(image_value, f"themedImages.images[{index}]")
        name = image.get("name")
        light = image.get("light")
        dark = image.get("dark")
        if not isinstance(name, str) or not THEMED_IMAGE_NAME.match(name):
            raise DesignError(f"themedImages.images[{index}].name must be PascalCase")
        if name in seen_names:
            raise DesignError(f"duplicate themed image name: {name}")
        seen_names.add(name)
        for variant_name, resource_name in (("light", light), ("dark", dark)):
            if not isinstance(resource_name, str) or not RESOURCE_NAME.match(resource_name):
                raise DesignError(f"themedImages.images[{index}].{variant_name} must be a resource name")
        if light == dark:
            raise DesignError(f"themed image {name} must use distinct light and dark resources")


def validate(tokens: dict | None = None) -> dict:
    tokens = tokens or load_tokens()
    validate_colors(tokens["colors"])
    validate_typography(tokens["typography"])
    validate_themed_images(tokens["themedImages"])
    return tokens


def lower_snake(value: str) -> str:
    result = []
    for char in value:
        if char.isupper() and result:
            result.append("_")
        result.append(char.lower())
    return "".join(result).replace(".", "_")


def android_color_name(parts: tuple[str, ...]) -> str:
    return "yalla_" + "_".join(lower_snake(part) for part in parts)


def split_words(value: str) -> list[str]:
    return [part for part in re.split(r"[_\-.]", lower_snake(value)) if part]


def pascal_case(value: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in split_words(value))


def camel_case(value: str) -> str:
    name = pascal_case(value)
    return name[:1].lower() + name[1:]


def swift_color_name(parts: tuple[str, ...]) -> str:
    head, *tail = parts
    return camel_case(head) + "".join(pascal_case(part) for part in tail)


def swift_case_name(value: str) -> str:
    return camel_case(value)


def kotlin_symbol(parts: tuple[str, ...]) -> str:
    scheme, group, token = parts
    # Preserve the existing internal CMP symbol used by ColorScheme.kt.
    if group == "background" and token == "brand":
        token = "brandBase"
    return pascal_case(scheme) + pascal_case(group) + pascal_case(token)


def kotlin_accent_symbol(token: str) -> str:
    return pascal_case(token)


def kotlin_gradient_symbol(token: str) -> str:
    return pascal_case(token) + "Background" if token == "splash" else pascal_case(token)


def argb_literal(color: str) -> str:
    return "0xFF" + color.removeprefix("#").upper()


def kotlin_color_literal(color: str) -> str:
    return f"Color({argb_literal(color)})"


def resource_alias_name(image_name: str) -> str:
    return "yalla_img_" + lower_snake(image_name)


def format_number(value: object) -> str:
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def kotlin_sp(value: object) -> str:
    return format_number(value) + ".sp"


def kotlin_float(value: object) -> str:
    if isinstance(value, int):
        return f"{value}.0f"
    if isinstance(value, float) and value.is_integer():
        return f"{int(value)}.0f"
    return f"{value}f"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate_metadata(tokens: dict, out_dir: Path) -> None:
    write_json(out_dir / "metadata" / "yalla-design.json", tokens)


def color_rows(colors: dict, scheme: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for group_name, group in colors["schemes"][scheme].items():
        for token_name, color in group.items():
            rows.append((android_color_name((group_name, token_name)), color))
    for token_name, color in colors["accent"].items():
        rows.append((android_color_name(("accent", token_name)), color))
    for gradient_name, stops in colors["gradients"].items():
        for index, stop in enumerate(stops):
            rows.append((android_color_name(("gradient", gradient_name, str(index))), stop["color"]))
    return rows


def generate_android_colors(tokens: dict, out_dir: Path) -> None:
    for folder, scheme in (("values", "light"), ("values-night", "dark")):
        rows = color_rows(tokens["colors"], scheme)
        lines = [
            "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
            "<!-- Generated by yalla-design. Do not edit manually. -->",
            "<resources>",
        ]
        lines.extend(f"    <color name=\"{name}\">{color}</color>" for name, color in rows)
        lines.append("</resources>")
        write_text(out_dir / "android" / "sdk" / "src" / "main" / "res" / folder / "yalla_colors.xml", "\n".join(lines) + "\n")


def generate_android_themed_image_aliases(tokens: dict, out_dir: Path) -> None:
    for folder, variant in (("values", "light"), ("values-night", "dark")):
        lines = [
            "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
            "<!-- Generated by yalla-design. Do not edit manually. -->",
            "<resources>",
        ]
        for image in tokens["themedImages"]["images"]:
            lines.append(
                f"    <item type=\"drawable\" name=\"{resource_alias_name(image['name'])}\">@drawable/{image[variant]}</item>"
            )
        lines.append("</resources>")
        write_text(out_dir / "android" / "sdk" / "src" / "main" / "res" / folder / "yalla_themed_images.xml", "\n".join(lines) + "\n")


def generate_android_color_helpers(tokens: dict, out_dir: Path) -> None:
    colors = tokens["colors"]
    lines = [
        "package uz.yalla.sdk.android.design",
        "",
        "import uz.yalla.sdk.android.R",
        "",
        "public object YallaColors {",
    ]
    for group_name, group in colors["schemes"]["light"].items():
        lines.append(f"    public object {pascal_case(group_name)} {{")
        for token_name in group:
            lines.append(f"        public val {camel_case(token_name)}: Int get() = R.color.{android_color_name((group_name, token_name))}")
        lines.append("    }")
        lines.append("")
    lines.append("    public object Accent {")
    for token_name, color in tokens["colors"]["accent"].items():
        del color
        lines.append(f"        public val {camel_case(token_name)}: Int get() = R.color.{android_color_name(('accent', token_name))}")
    lines.append("    }")
    lines.append("")
    lines.append("    public object Gradient {")
    for gradient_name, stops in colors["gradients"].items():
        resource_names = ", ".join(f"R.color.{android_color_name(('gradient', gradient_name, str(index)))}" for index, _ in enumerate(stops))
        lines.append(f"        public val {camel_case(gradient_name)}: IntArray get() = intArrayOf({resource_names})")
    lines.append("    }")
    lines.append("}")
    write_text(out_dir / "android" / "sdk" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "YallaColors.kt", "\n".join(lines) + "\n")


def generate_android_typography_helpers(tokens: dict, out_dir: Path) -> None:
    styles = tokens["typography"]["styles"]
    resources = tokens["typography"]["fontResources"]["android"]

    def style_expr(key: str) -> str:
        style = styles[key]
        return (
            f"YallaTextStyle(fontRes = R.font.{resources[style['font']]}, "
            f"sizeSp = {kotlin_float(style['sizeSp'])}, "
            f"lineHeightSp = {kotlin_float(style['lineHeightSp'])})"
        )

    lines = [
        "package uz.yalla.sdk.android.design",
        "",
        "import uz.yalla.sdk.android.R",
        "",
        "public data class YallaTextStyle(",
        "    public val fontRes: Int,",
        "    public val sizeSp: Float,",
        "    public val lineHeightSp: Float",
        ")",
        "",
        "public object YallaTypography {",
        "    public object Title {",
        f"        public val xLarge: YallaTextStyle = {style_expr('title.xLarge')}",
        f"        public val large: YallaTextStyle = {style_expr('title.large')}",
        f"        public val base: YallaTextStyle = {style_expr('title.base')}",
        "    }",
        "",
        "    public object Body {",
        f"        public val caption: YallaTextStyle = {style_expr('body.caption')}",
        "",
        "        public object Large {",
        f"            public val regular: YallaTextStyle = {style_expr('body.large.regular')}",
        f"            public val medium: YallaTextStyle = {style_expr('body.large.medium')}",
        f"            public val bold: YallaTextStyle = {style_expr('body.large.bold')}",
        "        }",
        "",
        "        public object Base {",
        f"            public val regular: YallaTextStyle = {style_expr('body.base.regular')}",
        f"            public val medium: YallaTextStyle = {style_expr('body.base.medium')}",
        f"            public val bold: YallaTextStyle = {style_expr('body.base.bold')}",
        "        }",
        "",
        "        public object Small {",
        f"            public val regular: YallaTextStyle = {style_expr('body.small.regular')}",
        f"            public val medium: YallaTextStyle = {style_expr('body.small.medium')}",
        f"            public val bold: YallaTextStyle = {style_expr('body.small.bold')}",
        "        }",
        "    }",
        "",
        "    public object Custom {",
        f"        public val carNumber: YallaTextStyle = {style_expr('custom.carNumber')}",
        "    }",
        "}",
    ]
    write_text(out_dir / "android" / "sdk" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "YallaTypography.kt", "\n".join(lines) + "\n")


def generate_android_themed_image_helpers(tokens: dict, out_dir: Path) -> None:
    lines = [
        "package uz.yalla.sdk.android.design",
        "",
        "import uz.yalla.sdk.android.R",
        "",
        "public enum class YallaThemedImage(public val resId: Int) {",
    ]
    images = tokens["themedImages"]["images"]
    for index, image in enumerate(images):
        suffix = "," if index < len(images) - 1 else ";"
        lines.append(f"    {image['name']}(R.drawable.{resource_alias_name(image['name'])}){suffix}")
    lines.append("}")
    write_text(out_dir / "android" / "sdk" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "YallaThemedImage.kt", "\n".join(lines) + "\n")


def generate_android_design(tokens: dict, out_dir: Path) -> None:
    generate_android_colors(tokens, out_dir)
    generate_android_themed_image_aliases(tokens, out_dir)
    generate_android_color_helpers(tokens, out_dir)
    generate_android_typography_helpers(tokens, out_dir)
    generate_android_themed_image_helpers(tokens, out_dir)


def generate_cmp_colors(tokens: dict, out_dir: Path) -> None:
    colors = tokens["colors"]
    lines = [
        "package uz.yalla.design.color",
        "",
        "import androidx.compose.ui.geometry.Offset",
        "import androidx.compose.ui.graphics.Brush",
        "import androidx.compose.ui.graphics.Color",
        "",
        "// Generated by yalla-design. Do not edit manually.",
        "",
    ]
    for scheme in ("light", "dark"):
        lines.append(f"// region {pascal_case(scheme)} Theme Colors")
        lines.append("")
        for group_name, group in colors["schemes"][scheme].items():
            for token_name, color in group.items():
                lines.append(f"internal val {kotlin_symbol((scheme, group_name, token_name))} = {kotlin_color_literal(color)}")
        lines.append("")
        lines.append("// endregion")
        lines.append("")
    lines.append("// region Accent Colors")
    lines.append("")
    for token_name, color in colors["accent"].items():
        lines.append(f"internal val {kotlin_accent_symbol(token_name)} = {kotlin_color_literal(color)}")
    lines.append("")
    lines.append("// endregion")
    lines.append("")
    lines.append("// region Gradients")
    lines.append("")
    for gradient_name, stops in colors["gradients"].items():
        symbol = kotlin_gradient_symbol(gradient_name)
        stop_values = ", ".join(kotlin_color_literal(stop["color"]) for stop in stops)
        if gradient_name == "splash":
            lines.extend(
                [
                    f"internal val {symbol} =",
                    "    Brush.linearGradient(",
                    f"        colors = listOf({stop_values}),",
                    "        start = Offset(0f, 0f),",
                    "        end = Offset(1000f, 1000f)",
                    "    )",
                ]
            )
        else:
            lines.append(f"internal val {symbol} = Brush.linearGradient(listOf({stop_values}))")
        lines.append("")
    lines.append("// endregion")
    write_text(
        out_dir / "cmp" / "design" / "src" / "commonMain" / "kotlin" / "uz" / "yalla" / "design" / "color" / "Color.kt",
        "\n".join(lines).rstrip() + "\n",
    )


def kotlin_font_ref(font_role: str) -> str:
    return "Res.font.nummernschild" if font_role == "carNumber" else f"{font_role}Font"


def kotlin_text_style(style: dict, indent: int) -> list[str]:
    space = " " * indent
    inner = " " * (indent + 4)
    return [
        f"{space}TextStyle(",
        f"{inner}fontSize = {kotlin_sp(style['sizeSp'])},",
        f"{inner}lineHeight = {kotlin_sp(style['lineHeightSp'])},",
        f"{inner}fontFamily = FontFamily(Font({kotlin_font_ref(style['font'])}))",
        f"{space})",
    ]


def with_comma(lines: list[str]) -> list[str]:
    copied = list(lines)
    copied[-1] += ","
    return copied


def generate_cmp_font_common(tokens: dict, out_dir: Path) -> None:
    styles = tokens["typography"]["styles"]
    lines = [
        "package uz.yalla.design.font",
        "",
        "import androidx.compose.runtime.Composable",
        "import androidx.compose.ui.text.TextStyle",
        "import androidx.compose.ui.text.font.FontFamily",
        "import androidx.compose.ui.unit.sp",
        "import org.jetbrains.compose.resources.Font",
        "import org.jetbrains.compose.resources.FontResource",
        "import uz.yalla.resources.Res",
        "import uz.yalla.resources.nummernschild",
        "",
        "// Generated by yalla-design. Do not edit manually.",
        "",
        "expect val boldFont: FontResource",
        "expect val mediumFont: FontResource",
        "expect val normalFont: FontResource",
        "",
        "@Composable",
        "fun rememberFontScheme(): FontScheme =",
        "    FontScheme(",
        "        title =",
        "            FontScheme.Title(",
        "                xLarge =",
        *with_comma(kotlin_text_style(styles["title.xLarge"], 20)),
        "                large =",
        *with_comma(kotlin_text_style(styles["title.large"], 20)),
        "                base =",
        *kotlin_text_style(styles["title.base"], 20),
        "            ),",
        "        body =",
        "            FontScheme.Body(",
        "                caption =",
        *with_comma(kotlin_text_style(styles["body.caption"], 20)),
        "                large =",
        "                    FontScheme.Body.Weighty(",
        "                        regular =",
        *with_comma(kotlin_text_style(styles["body.large.regular"], 28)),
        "                        medium =",
        *with_comma(kotlin_text_style(styles["body.large.medium"], 28)),
        "                        bold =",
        *kotlin_text_style(styles["body.large.bold"], 28),
        "                    ),",
        "                base =",
        "                    FontScheme.Body.Weighty(",
        "                        regular =",
        *with_comma(kotlin_text_style(styles["body.base.regular"], 28)),
        "                        medium =",
        *with_comma(kotlin_text_style(styles["body.base.medium"], 28)),
        "                        bold =",
        *kotlin_text_style(styles["body.base.bold"], 28),
        "                    ),",
        "                small =",
        "                    FontScheme.Body.Weighty(",
        "                        regular =",
        *with_comma(kotlin_text_style(styles["body.small.regular"], 28)),
        "                        medium =",
        *with_comma(kotlin_text_style(styles["body.small.medium"], 28)),
        "                        bold =",
        *kotlin_text_style(styles["body.small.bold"], 28),
        "                    )",
        "            ),",
        "        custom =",
        "            FontScheme.Custom(",
        "                carNumber =",
        *kotlin_text_style(styles["custom.carNumber"], 20),
        "            )",
        "    )",
    ]
    write_text(
        out_dir / "cmp" / "design" / "src" / "commonMain" / "kotlin" / "uz" / "yalla" / "design" / "font" / "Font.kt",
        "\n".join(lines) + "\n",
    )


def generate_cmp_font_platform(tokens: dict, out_dir: Path, platform: str, source_set: str) -> None:
    resources = tokens["typography"]["fontResources"][platform]
    lines = [
        "package uz.yalla.design.font",
        "",
        "import org.jetbrains.compose.resources.FontResource",
        "import uz.yalla.resources.Res",
        f"import uz.yalla.resources.{resources['bold']}",
        f"import uz.yalla.resources.{resources['medium']}",
        f"import uz.yalla.resources.{resources['normal']}",
        "",
        "// Generated by yalla-design. Do not edit manually.",
        "",
        f"actual val boldFont: FontResource = Res.font.{resources['bold']}",
        f"actual val mediumFont: FontResource = Res.font.{resources['medium']}",
        f"actual val normalFont: FontResource = Res.font.{resources['normal']}",
    ]
    write_text(
        out_dir / "cmp" / "design" / "src" / source_set / "kotlin" / "uz" / "yalla" / "design" / "font" / f"Font.{source_set.removesuffix('Main')}.kt",
        "\n".join(lines) + "\n",
    )


def generate_cmp_themed_images(tokens: dict, out_dir: Path) -> None:
    images = tokens["themedImages"]["images"]
    resource_names = sorted({image["light"] for image in images} | {image["dark"] for image in images})
    lines = [
        "package uz.yalla.design.image",
        "",
        "import org.jetbrains.compose.resources.DrawableResource",
        "import uz.yalla.resources.Res",
        *[f"import uz.yalla.resources.{resource_name}" for resource_name in resource_names],
        "",
        "// Generated by yalla-design. Do not edit manually.",
        "",
        "enum class ThemedImage(",
        "    val light: DrawableResource,",
        "    val dark: DrawableResource",
        ") {",
    ]
    for index, image in enumerate(images):
        suffix = "," if index < len(images) - 1 else ""
        lines.append(f"    {image['name']}(Res.drawable.{image['light']}, Res.drawable.{image['dark']}){suffix}")
    lines.append("}")
    write_text(
        out_dir / "cmp" / "design" / "src" / "commonMain" / "kotlin" / "uz" / "yalla" / "design" / "image" / "ThemedImage.kt",
        "\n".join(lines) + "\n",
    )


def generate_cmp_design(tokens: dict, out_dir: Path) -> None:
    generate_cmp_colors(tokens, out_dir)
    generate_cmp_font_common(tokens, out_dir)
    generate_cmp_font_platform(tokens, out_dir, "cmpAndroid", "androidMain")
    generate_cmp_font_platform(tokens, out_dir, "cmpIos", "iosMain")
    generate_cmp_themed_images(tokens, out_dir)


def generate_ios_colors(tokens: dict, out_dir: Path) -> None:
    colors = tokens["colors"]
    lines = [
        "import SwiftUI",
        "#if canImport(UIKit)",
        "import UIKit",
        "public typealias YallaNativeColor = UIColor",
        "#elseif canImport(AppKit)",
        "import AppKit",
        "public typealias YallaNativeColor = NSColor",
        "#endif",
        "",
        "// Generated by yalla-design. Do not edit manually.",
        "",
        "public enum YallaUIColor {",
    ]
    for group_name, group in colors["schemes"]["light"].items():
        for token_name, light_color in group.items():
            dark_color = colors["schemes"]["dark"][group_name][token_name]
            lines.append(
                f"    public static let {swift_color_name((group_name, token_name))}: YallaNativeColor = dynamic(light: {argb_literal(light_color)}, dark: {argb_literal(dark_color)})"
            )
    for token_name, color in colors["accent"].items():
        lines.append(f"    public static let {swift_color_name(('accent', token_name))}: YallaNativeColor = fixed({argb_literal(color)})")
    for gradient_name, stops in colors["gradients"].items():
        values = ", ".join(f"fixed({argb_literal(stop['color'])})" for stop in stops)
        lines.append(f"    public static let {swift_color_name(('gradient', gradient_name))}: [YallaNativeColor] = [{values}]")
    lines.extend(
        [
            "",
            "    private static func dynamic(light: UInt32, dark: UInt32) -> YallaNativeColor {",
            "        #if canImport(UIKit)",
            "        return UIColor { traitCollection in",
            "            return traitCollection.userInterfaceStyle == .dark ? color(dark) : color(light)",
            "        }",
            "        #elseif canImport(AppKit)",
            "        return NSColor(name: nil) { appearance in",
            "            let bestMatch = appearance.bestMatch(from: [.aqua, .darkAqua])",
            "            return bestMatch == .darkAqua ? color(dark) : color(light)",
            "        }",
            "        #endif",
            "    }",
            "",
            "    private static func fixed(_ argb: UInt32) -> YallaNativeColor {",
            "        return color(argb)",
            "    }",
            "",
            "    private static func color(_ argb: UInt32) -> YallaNativeColor {",
            "        #if canImport(UIKit)",
            "        return UIColor(",
            "            red: CGFloat((argb >> 16) & 0xFF) / 255.0,",
            "            green: CGFloat((argb >> 8) & 0xFF) / 255.0,",
            "            blue: CGFloat(argb & 0xFF) / 255.0,",
            "            alpha: CGFloat((argb >> 24) & 0xFF) / 255.0",
            "        )",
            "        #elseif canImport(AppKit)",
            "        return NSColor(",
            "            red: CGFloat((argb >> 16) & 0xFF) / 255.0,",
            "            green: CGFloat((argb >> 8) & 0xFF) / 255.0,",
            "            blue: CGFloat(argb & 0xFF) / 255.0,",
            "            alpha: CGFloat((argb >> 24) & 0xFF) / 255.0",
            "        )",
            "        #endif",
            "    }",
            "}",
            "",
            "public enum YallaColor {",
        ]
    )
    for group_name, group in colors["schemes"]["light"].items():
        for token_name in group:
            name = swift_color_name((group_name, token_name))
            lines.append(f"    public static let {name}: Color = platformColor(YallaUIColor.{name})")
    for token_name in colors["accent"]:
        name = swift_color_name(("accent", token_name))
        lines.append(f"    public static let {name}: Color = platformColor(YallaUIColor.{name})")
    lines.extend(
        [
            "",
            "    private static func platformColor(_ color: YallaNativeColor) -> Color {",
            "        #if canImport(UIKit)",
            "        return Color(uiColor: color)",
            "        #elseif canImport(AppKit)",
            "        return Color(nsColor: color)",
            "        #endif",
            "    }",
        ]
    )
    lines.append("}")
    write_text(out_dir / "ios" / "Sources" / "YallaDesignIOS" / "YallaColors.swift", "\n".join(lines) + "\n")


def generate_ios_typography(tokens: dict, out_dir: Path) -> None:
    styles = tokens["typography"]["styles"]
    resources = tokens["typography"]["fontResources"]["ios"]

    def style_expr(key: str) -> str:
        style = styles[key]
        return (
            f"YallaTextStyle(fontResourceName: \"{resources[style['font']]}\", "
            f"size: {format_number(style['sizeSp'])}, "
            f"lineHeight: {format_number(style['lineHeightSp'])})"
        )

    lines = [
        "import CoreGraphics",
        "import CoreText",
        "import SwiftUI",
        "#if canImport(UIKit)",
        "import UIKit",
        "public typealias YallaNativeFont = UIFont",
        "#elseif canImport(AppKit)",
        "import AppKit",
        "public typealias YallaNativeFont = NSFont",
        "#endif",
        "import YallaResourcesIOS",
        "",
        "// Generated by yalla-design. Do not edit manually.",
        "",
        "public struct YallaTextStyle: Sendable {",
        "    public let fontResourceName: String",
        "    public let size: CGFloat",
        "    public let lineHeight: CGFloat",
        "",
        "    public init(fontResourceName: String, size: CGFloat, lineHeight: CGFloat) {",
        "        self.fontResourceName = fontResourceName",
        "        self.size = size",
        "        self.lineHeight = lineHeight",
        "    }",
        "",
        "    public var nativeFont: YallaNativeFont {",
        "        if let url = YallaResourcesIOS.fontURL(fontResourceName),",
        "           let provider = CGDataProvider(url: url as CFURL),",
        "           let cgFont = CGFont(provider) {",
        "            let ctFont = CTFontCreateWithGraphicsFont(cgFont, size, nil, nil)",
        "            let descriptor = CTFontCopyFontDescriptor(ctFont)",
        "            #if canImport(UIKit)",
        "            return UIFont(descriptor: descriptor as UIFontDescriptor, size: size)",
        "            #elseif canImport(AppKit)",
        "            return NSFont(descriptor: descriptor as NSFontDescriptor, size: size) ?? NSFont.systemFont(ofSize: size)",
        "            #endif",
        "        }",
        "        #if canImport(UIKit)",
        "        return UIFont.systemFont(ofSize: size)",
        "        #elseif canImport(AppKit)",
        "        return NSFont.systemFont(ofSize: size)",
        "        #endif",
        "    }",
        "",
        "    #if canImport(UIKit)",
        "    public var uiFont: UIFont { nativeFont }",
        "    #elseif canImport(AppKit)",
        "    public var nsFont: NSFont { nativeFont }",
        "    #endif",
        "",
        "    public var swiftUIFont: Font {",
        "        Font.custom(fontResourceName, size: size)",
        "    }",
        "}",
        "",
        "public enum YallaTypography {",
        "    public enum Title {",
        f"        public static let xLarge = {style_expr('title.xLarge')}",
        f"        public static let large = {style_expr('title.large')}",
        f"        public static let base = {style_expr('title.base')}",
        "    }",
        "",
        "    public enum Body {",
        f"        public static let caption = {style_expr('body.caption')}",
        "",
        "        public enum Large {",
        f"            public static let regular = {style_expr('body.large.regular')}",
        f"            public static let medium = {style_expr('body.large.medium')}",
        f"            public static let bold = {style_expr('body.large.bold')}",
        "        }",
        "",
        "        public enum Base {",
        f"            public static let regular = {style_expr('body.base.regular')}",
        f"            public static let medium = {style_expr('body.base.medium')}",
        f"            public static let bold = {style_expr('body.base.bold')}",
        "        }",
        "",
        "        public enum Small {",
        f"            public static let regular = {style_expr('body.small.regular')}",
        f"            public static let medium = {style_expr('body.small.medium')}",
        f"            public static let bold = {style_expr('body.small.bold')}",
        "        }",
        "    }",
        "",
        "    public enum Custom {",
        f"        public static let carNumber = {style_expr('custom.carNumber')}",
        "    }",
        "}",
    ]
    write_text(out_dir / "ios" / "Sources" / "YallaDesignIOS" / "YallaTypography.swift", "\n".join(lines) + "\n")


def generate_ios_themed_images(tokens: dict, out_dir: Path) -> None:
    images = tokens["themedImages"]["images"]
    lines = [
        "import SwiftUI",
        "#if canImport(UIKit)",
        "import UIKit",
        "#elseif canImport(AppKit)",
        "import AppKit",
        "#endif",
        "import YallaResourcesIOS",
        "",
        "// Generated by yalla-design. Do not edit manually.",
        "",
        "public enum YallaThemedImage: String, CaseIterable, Sendable {",
    ]
    for image in images:
        lines.append(f"    case {swift_case_name(image['name'])} = \"{image['name']}\"")
    lines.extend(
        [
            "",
            "    public var assetName: String {",
            "        switch self {",
        ]
    )
    for image in images:
        lines.append(f"        case .{swift_case_name(image['name'])}:")
        lines.append(f"            return \"{resource_alias_name(image['name'])}\"")
    lines.extend(
        [
            "        }",
            "    }",
            "",
            "    #if canImport(UIKit)",
            "    public func uiImage(compatibleWith traitCollection: UITraitCollection? = nil) -> UIImage? {",
            "        return YallaResourcesIOS.platformImage(assetName, compatibleWith: traitCollection)",
            "    }",
            "    #elseif canImport(AppKit)",
            "    public func nsImage() -> NSImage? {",
            "        return YallaResourcesIOS.platformImage(assetName)",
            "    }",
            "    #endif",
            "",
            "    @available(iOS 13.0, macOS 10.15, *)",
            "    public var image: Image {",
            "        YallaResourcesIOS.swiftUIImage(assetName)",
            "    }",
            "}",
        ]
    )
    write_text(out_dir / "ios" / "Sources" / "YallaDesignIOS" / "YallaThemedImage.swift", "\n".join(lines) + "\n")


def generate_ios_design(tokens: dict, out_dir: Path) -> None:
    generate_ios_colors(tokens, out_dir)
    generate_ios_typography(tokens, out_dir)
    generate_ios_themed_images(tokens, out_dir)


def generate(out_dir: Path, tokens: dict | None = None) -> None:
    tokens = validate(tokens)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    generate_metadata(tokens, out_dir)
    generate_cmp_design(tokens, out_dir)
    generate_android_design(tokens, out_dir)
    generate_ios_design(tokens, out_dir)


def copy_generated_tree(source: Path, destination: Path) -> list[Path]:
    if not source.exists():
        raise DesignError(f"generated source does not exist: {source}")
    if not destination.exists():
        raise DesignError(f"destination repo does not exist: {destination}")
    written: list[Path] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(source)
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        written.append(target)
    return written


def sync(cmp_root: Path, android_root: Path, ios_root: Path) -> dict[str, list[Path]]:
    tokens = validate()
    with tempfile.TemporaryDirectory() as generated_dir:
        generated = Path(generated_dir) / "generated"
        generate(generated, tokens)
        return {
            "cmp": copy_generated_tree(generated / "cmp", cmp_root),
            "android": copy_generated_tree(generated / "android", android_root),
            "ios": copy_generated_tree(generated / "ios", ios_root),
        }


def check() -> None:
    tokens = validate()
    with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
        first = Path(first_dir) / "generated"
        second = Path(second_dir) / "generated"
        generate(first, tokens)
        generate(second, tokens)
        first_files = sorted(path.relative_to(first) for path in first.rglob("*") if path.is_file())
        second_files = sorted(path.relative_to(second) for path in second.rglob("*") if path.is_file())
        if first_files != second_files:
            raise DesignError("generated file list is not deterministic")
        for relative_path in first_files:
            if (first / relative_path).read_bytes() != (second / relative_path).read_bytes():
                raise DesignError(f"generated file is not deterministic: {relative_path}")
        for relative_path in (
            Path("android/sdk/src/main/res/values/yalla_colors.xml"),
            Path("android/sdk/src/main/res/values-night/yalla_colors.xml"),
            Path("android/sdk/src/main/res/values/yalla_themed_images.xml"),
            Path("android/sdk/src/main/res/values-night/yalla_themed_images.xml"),
        ):
            ElementTree.parse(first / relative_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and generate Yalla design outputs")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--out", type=Path, default=ROOT / "build" / "generated")
    sync_parser = subparsers.add_parser("sync")
    default_projects_root = ROOT.parent
    sync_parser.add_argument("--cmp-root", type=Path, default=default_projects_root / "yalla-sdk")
    sync_parser.add_argument("--android-root", type=Path, default=default_projects_root / "yalla-sdk-android")
    sync_parser.add_argument("--ios-root", type=Path, default=default_projects_root / "yalla-sdk-ios")
    subparsers.add_parser("check")
    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            validate()
            print("Design tokens are valid")
        elif args.command == "generate":
            generate(args.out)
            print(f"Generated design outputs into {args.out}")
        elif args.command == "sync":
            written = sync(args.cmp_root, args.android_root, args.ios_root)
            for target, paths in written.items():
                print(f"Synced {len(paths)} design files to {target}")
        elif args.command == "check":
            check()
            print("Design generator check passed")
        else:
            parser.error(f"unknown command: {args.command}")
    except DesignError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
