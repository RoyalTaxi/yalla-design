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
                out / "cmp" / "design" / "src" / "androidMain" / "kotlin" / "uz" / "yalla" / "design" / "font" / "Font.android.kt",
                out / "cmp" / "design" / "src" / "iosMain" / "kotlin" / "uz" / "yalla" / "design" / "font" / "Font.ios.kt",
                out / "cmp" / "design" / "src" / "commonMain" / "kotlin" / "uz" / "yalla" / "design" / "image" / "ThemedImage.kt",
                out / "android" / "design" / "src" / "main" / "res" / "values" / "colors.xml",
                out / "android" / "design" / "src" / "main" / "res" / "values-night" / "colors.xml",
                out / "android" / "design" / "src" / "main" / "res" / "drawable" / "yalla_img_login.xml",
                out / "android" / "design" / "src" / "main" / "res" / "drawable-night" / "yalla_img_login.xml",
                out / "android" / "design" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "YallaColors.kt",
                out / "android" / "design" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "YallaFonts.kt",
                out / "android" / "design" / "src" / "main" / "kotlin" / "uz" / "yalla" / "sdk" / "android" / "design" / "YallaThemedImage.kt",
                out / "ios" / "Sources" / "YallaDesignIOS" / "YallaColors.swift",
                out / "ios" / "Sources" / "YallaDesignIOS" / "YallaFonts.swift",
                out / "ios" / "Sources" / "YallaDesignIOS" / "YallaThemedImage.swift",
            ]
            for path in expected:
                self.assertTrue(path.exists(), f"missing generated file: {path}")

            ElementTree.parse(out / "android" / "design" / "src" / "main" / "res" / "values" / "colors.xml")
            ElementTree.parse(out / "android" / "design" / "src" / "main" / "res" / "values-night" / "colors.xml")
            ElementTree.parse(out / "android" / "design" / "src" / "main" / "res" / "drawable" / "yalla_img_login.xml")

            metadata = json.loads((out / "metadata" / "yalla-design.json").read_text(encoding="utf-8"))
            self.assertEqual(12, len(metadata["themedImages"]["images"]))

    def test_check_is_deterministic(self):
        yalla_design.check()


if __name__ == "__main__":
    unittest.main()
