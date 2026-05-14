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
        
        # Verify Kotlin files exist for both platforms
        for platform in ["cmp", "android"]:
            for folder in ["color", "font", "theme", "image"]:
                if platform == "cmp":
                    kotlin_path = first / platform / "design" / "src" / "commonMain" / "kotlin" / "uz" / "yalla" / "design" / folder
                else:
                    kotlin_path = first / platform / "design" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / folder
                if not kotlin_path.exists():
                    raise DesignError(f"missing {folder} directory for {platform}: {kotlin_path}")

        # Verify a themed image drawable exists (prefix 'img_' used)
        themed_img = first / "android/design/src/main/res/drawable/img_login.xml"
        if not themed_img.exists():
            raise DesignError(f"missing themed image drawable: {themed_img}")
        ElementTree.parse(themed_img)

