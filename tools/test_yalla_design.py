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
        self.assertIn("fonts", tokens)
        self.assertIn("themedImages", tokens)

    def test_generate_expected_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "generated"
            yalla_design.generate(out)

            expected = [
                out / "metadata" / "yalla-design.json",
                out / "cmp" / "design" / "src" / "commonMain" / "kotlin" / "uz" / "yalla" / "design" / "color" / "Color.kt",
                out / "cmp" / "design" / "src" / "commonMain" / "kotlin" / "uz" / "yalla" / "design" / "font" / "Font.kt",
                out / "cmp" / "design" / "src" / "commonMain" / "kotlin" / "uz" / "yalla" / "design" / "image" / "ThemedImage.kt",
                out / "android" / "design" / "src" / "main" / "res" / "drawable" / "img_login.xml",
                out / "android" / "design" / "src" / "main" / "res" / "drawable-night" / "img_login.xml",
                out / "android" / "design" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "color" / "Color.kt",
                out / "android" / "design" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "font" / "Font.kt",
                out / "android" / "design" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "image" / "ThemedImage.kt",
                out / "ios" / "Sources" / "Design" / "YallaFonts.swift",
                out / "ios" / "Sources" / "Resources" / "Resources" / "YallaColors.xcassets" / "text_base.colorset" / "Contents.json",
                out / "ios" / "Sources" / "Resources" / "Resources" / "YallaColors.xcassets" / "accent_pink_sun.colorset" / "Contents.json",
            ]
            for path in expected:
                self.assertTrue(path.exists(), f"missing generated file: {path}")

            self.assertFalse(
                (out / "ios" / "Sources" / "Design" / "YallaColors.swift").exists()
            )
            self.assertFalse(
                (out / "ios" / "Sources" / "Design" / "YallaThemedImage.swift").exists()
            )

            ElementTree.parse(out / "android" / "design" / "src" / "main" / "res" / "drawable" / "img_login.xml")

            metadata = json.loads((out / "metadata" / "yalla-design.json").read_text(encoding="utf-8"))
            self.assertEqual(12, len(metadata["themedImages"]["images"]))

    def test_check_is_deterministic(self):
        yalla_design.check()


if __name__ == "__main__":
    unittest.main()
