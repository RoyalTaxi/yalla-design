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


def generated_header(comment: str) -> str:
    return f"{comment}\n{comment.replace(comment[0], comment[0], 1)} Generated by yalla-design. Do not edit manually.\n"


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
    if scheme == "light":
        for token_name, color in colors["accent"].items():
            rows.append((android_color_name(("accent", token_name)), color))
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
        write_text(out_dir / "android" / "res" / folder / "yalla_colors.xml", "\n".join(lines) + "\n")


def swift_color_name(parts: tuple[str, ...]) -> str:
    head, *tail = parts
    return head + "".join(part[:1].upper() + part[1:] for part in tail)


def generate_ios_colors(tokens: dict, out_dir: Path) -> None:
    lines = [
        "// Generated by yalla-design. Do not edit manually.",
        "import Foundation",
        "",
        "public enum YallaColorToken {",
    ]
    for scheme in ("light", "dark"):
        for group_name, group in tokens["colors"]["schemes"][scheme].items():
            for token_name, color in group.items():
                swift_name = swift_color_name((scheme, group_name, token_name))
                lines.append(f"    public static let {swift_name}: UInt32 = 0xFF{color.removeprefix('#')}")
    for token_name, color in tokens["colors"]["accent"].items():
        swift_name = swift_color_name(("accent", token_name))
        lines.append(f"    public static let {swift_name}: UInt32 = 0xFF{color.removeprefix('#')}")
    lines.append("}")
    write_text(out_dir / "ios" / "Sources" / "YallaDesignIOS" / "YallaColorToken.swift", "\n".join(lines) + "\n")


def kotlin_const_name(parts: tuple[str, ...]) -> str:
    return "_".join(lower_snake(part).upper() for part in parts)


def generate_cmp_colors(tokens: dict, out_dir: Path) -> None:
    lines = [
        "// Generated by yalla-design. Do not edit manually.",
        "package uz.yalla.design.generated",
        "",
        "internal object YallaColorToken {",
    ]
    for scheme in ("light", "dark"):
        for group_name, group in tokens["colors"]["schemes"][scheme].items():
            for token_name, color in group.items():
                name = kotlin_const_name((scheme, group_name, token_name))
                lines.append(f"    const val {name}: ULong = 0xFF{color.removeprefix('#')}u")
    for token_name, color in tokens["colors"]["accent"].items():
        name = kotlin_const_name(("accent", token_name))
        lines.append(f"    const val {name}: ULong = 0xFF{color.removeprefix('#')}u")
    lines.append("}")
    write_text(out_dir / "cmp" / "kotlin" / "YallaColorToken.kt", "\n".join(lines) + "\n")


def generate_typography(tokens: dict, out_dir: Path) -> None:
    typography = tokens["typography"]
    write_json(out_dir / "android" / "typography.json", typography)
    write_json(out_dir / "ios" / "typography.json", typography)
    write_json(out_dir / "cmp" / "typography.json", typography)


def generate_themed_images(tokens: dict, out_dir: Path) -> None:
    themed_images = tokens["themedImages"]
    write_json(out_dir / "android" / "themed-images.json", themed_images)
    write_json(out_dir / "ios" / "themed-images.json", themed_images)
    write_json(out_dir / "cmp" / "themed-images.json", themed_images)


def generate(out_dir: Path, tokens: dict | None = None) -> None:
    tokens = validate(tokens)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    generate_metadata(tokens, out_dir)
    generate_android_colors(tokens, out_dir)
    generate_ios_colors(tokens, out_dir)
    generate_cmp_colors(tokens, out_dir)
    generate_typography(tokens, out_dir)
    generate_themed_images(tokens, out_dir)


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
            Path("android/res/values/yalla_colors.xml"),
            Path("android/res/values-night/yalla_colors.xml"),
        ):
            ElementTree.parse(first / relative_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and generate Yalla design outputs")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--out", type=Path, default=ROOT / "build" / "generated")
    subparsers.add_parser("check")
    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            validate()
            print("Design tokens are valid")
        elif args.command == "generate":
            generate(args.out)
            print(f"Generated design outputs into {args.out}")
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
