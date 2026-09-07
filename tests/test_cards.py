import unittest
import xml.etree.ElementTree as ET
from scripts.cards import wrap, frame, THEMES


class CardTests(unittest.TestCase):
    def test_long_unbroken_description_terminates_and_fits(self):
        lines = wrap("x" * 100 + " another word", 12, 70, 1)
        self.assertTrue(lines[0].endswith("…"))
        self.assertLessEqual(len(lines[0]) * 12 * .53, 70)

    def test_text_is_escaped_in_accessible_svg_label(self):
        svg = frame(100, 80, THEMES["dark"], "", 'A < B & "quoted"')
        root = ET.fromstring(svg)
        self.assertEqual(root.attrib["aria-label"], 'A < B & "quoted"')

    def test_short_description_is_preserved(self):
        self.assertEqual(wrap("A small project", 12, 300, 2), ["A small project"])
