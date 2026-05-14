from __future__ import annotations
import re

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
RESOURCE_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
THEMED_IMAGE_NAME = re.compile(r"^[A-Z][A-Za-z0-9]*$")

def lower_snake(value: str) -> str:
    result = []
    for char in value:
        if char.isupper() and result:
            result.append("_")
        result.append(char.lower())
    return "".join(result).replace(".", "_")

def split_words(value: str) -> list[str]:
    return [part for part in re.split(r"[_\-.]", lower_snake(value)) if part]

def pascal_case(value: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in split_words(value))

def camel_case(value: str) -> str:
    name = pascal_case(value)
    return name[:1].lower() + name[1:]

def android_color_name(parts: tuple[str, ...]) -> str:
    return "yalla_" + "_".join(lower_snake(part) for part in parts)

def swift_color_name(parts: tuple[str, ...]) -> str:
    head, *tail = parts
    return camel_case(head) + "".join(pascal_case(part) for part in tail)

def swift_case_name(value: str) -> str:
    return camel_case(value)

def kotlin_symbol(parts: tuple[str, ...]) -> str:
    scheme, group, token = parts
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
    from .formatters import argb_literal # type: ignore
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

def kotlin_font_ref(font_role: str) -> str:
    return "Res.font.nummernschild" if font_role == "carNumber" else f"{font_role}Font"

def kotlin_float(value: object) -> str:
    if isinstance(value, int):
        return f"{value}.0f"
    if isinstance(value, float) and value.is_integer():
        return f"{int(value)}.0f"
    return f"{value}f"
