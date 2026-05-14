import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

import yalla_design


class YallaDesignTest(unittest.TestCase):
    def test_validate_current_tokens(self):
        tokens = yalla_design.validate()
        self.assertIn("colors", tokens)
        self.assertIn("typography", tokens)
        self.assertIn("themedImages", tokens)

    def test_generate_expected_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "generated"
            yalla_design.generate(out)

            expected = [
                out / "metadata" / "yalla-design.json",
                out / "android" / "res" / "values" / "yalla_colors.xml",
                out / "android" / "res" / "values-night" / "yalla_colors.xml",
                out / "ios" / "Sources" / "YallaDesignIOS" / "YallaColorToken.swift",
                out / "cmp" / "kotlin" / "YallaColorToken.kt",
                out / "android" / "typography.json",
                out / "ios" / "typography.json",
                out / "cmp" / "typography.json",
                out / "android" / "themed-images.json",
                out / "ios" / "themed-images.json",
                out / "cmp" / "themed-images.json",
            ]
            for path in expected:
                self.assertTrue(path.exists(), f"missing generated file: {path}")

            ElementTree.parse(out / "android" / "res" / "values" / "yalla_colors.xml")
            ElementTree.parse(out / "android" / "res" / "values-night" / "yalla_colors.xml")

            metadata = json.loads((out / "metadata" / "yalla-design.json").read_text(encoding="utf-8"))
            self.assertEqual(12, len(metadata["themedImages"]["images"]))

    def test_check_is_deterministic(self):
        yalla_design.check()


if __name__ == "__main__":
    unittest.main()
