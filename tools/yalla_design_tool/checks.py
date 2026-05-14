from __future__ import annotations
import tempfile
from pathlib import Path
from xml.etree import ElementTree
from .io import DesignError
from .emitters import generate
from .validation import validate

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
