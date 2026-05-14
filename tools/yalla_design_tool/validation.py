from __future__ import annotations
from pathlib import Path
from .io import load_json, DesignError
from .formatters import HEX_COLOR, RESOURCE_NAME, THEMED_IMAGE_NAME
from .paths import TOKENS_DIR

def load_tokens(tokens_dir: Path = TOKENS_DIR) -> dict:
    return {
        "colors": load_json(tokens_dir / "colors.json"),
        "fonts": load_json(tokens_dir / "fonts.json"),
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

def validate_fonts(fonts: dict) -> None:
    font_resources = require_dict(fonts.get("fontResources"), "fonts.fontResources")
    required_platforms = {"android", "ios", "cmpAndroid", "cmpIos"}
    if set(font_resources) != required_platforms:
        raise DesignError(f"fonts.fontResources must contain {sorted(required_platforms)}")

    required_roles = {"normal", "medium", "bold", "carNumber"}
    for platform, resources_value in font_resources.items():
        resources = require_dict(resources_value, f"fonts.fontResources.{platform}")
        if set(resources) != required_roles:
            raise DesignError(f"fonts.fontResources.{platform} must contain {sorted(required_roles)}")
        for role, resource_name in resources.items():
            if not isinstance(resource_name, str) or not RESOURCE_NAME.match(resource_name):
                raise DesignError(f"fonts.fontResources.{platform}.{role} must be a resource name")

    styles = require_dict(fonts.get("styles"), "fonts.styles")
    if not styles:
        raise DesignError("fonts.styles must not be empty")
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
        raise DesignError(f"fonts.styles is missing required styles: {missing_styles}")
    for style_name, style_value in styles.items():
        style = require_dict(style_value, f"fonts.styles.{style_name}")
        font = style.get("font")
        if font not in required_roles:
            raise DesignError(f"fonts.styles.{style_name}.font must be one of {sorted(required_roles)}")
        for metric in ("sizeSp", "lineHeightSp"):
            value = style.get(metric)
            if not isinstance(value, (int, float)) or value <= 0:
                raise DesignError(f"fonts.styles.{style_name}.{metric} must be a positive number")

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
    validate_fonts(tokens["fonts"])
    validate_themed_images(tokens["themedImages"])
    return tokens
