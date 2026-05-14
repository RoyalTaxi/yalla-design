#!/usr/bin/env python3
from yalla_design_tool.cli import main
from yalla_design_tool.validation import validate
from yalla_design_tool.emitters import generate
from yalla_design_tool.sync import sync
from yalla_design_tool.checks import check

if __name__ == "__main__":
    import sys
    sys.exit(main())
