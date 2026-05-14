from __future__ import annotations
import shutil
import tempfile
from pathlib import Path
from .io import DesignError
from .emitters import generate
from .validation import validate

def copy_generated_tree(source: Path, destination: Path) -> list[Path]:
    if not source.exists():
        raise DesignError(f"generated source does not exist: {source}")
    if not destination.exists():
        raise DesignError(f"destination repo does not exist: {destination}")

    # Cleanup stale files if this is the Android repo
    if (destination / "sdk/src/main/res").exists():
        res_dir = destination / "sdk/src/main/res"
        for folder in ["values", "values-night"]:
            for name in ["yalla_colors.xml", "yalla_themed_images.xml"]:
                stale = res_dir / folder / name
                if stale.exists():
                    stale.unlink()
        # Also cleanup old Kotlin helpers in sdk module
        kotlin_base = destination / "sdk/src/main/kotlin/uz/yalla/sdk/android/design"
        if kotlin_base.exists():
            shutil.rmtree(kotlin_base)

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
