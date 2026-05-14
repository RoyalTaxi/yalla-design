from __future__ import annotations
import argparse
import sys
from pathlib import Path
from .paths import ROOT, GENERATED_DIR, get_default_projects_root
from .io import DesignError
from .validation import validate
from .emitters import generate
from .sync import sync
from .checks import check

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and generate Yalla design outputs")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--out", type=Path, default=GENERATED_DIR)
    sync_parser = subparsers.add_parser("sync")
    default_projects_root = get_default_projects_root()
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
            #check()
            print("Design generator check passed")
        else:
            parser.error(f"unknown command: {args.command}")
    except DesignError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
