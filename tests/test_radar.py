import contextlib
import io
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.radar import main, render


class RadarTests(unittest.TestCase):
    def test_quoted_titles_and_axis_labels_produce_valid_accessible_svg(self):
        title = 'My "skills" < & >'
        axes = [('A & B', 25), ('"C"', 50), ('<D>', 75)]
        for theme in ('light', 'dark'):
            svg = render(title, axes, theme, 440, 4, True, False)
            root = ET.fromstring(svg)
            self.assertEqual(root.attrib['aria-label'], title)
            texts = [node.text for node in root.iter('{http://www.w3.org/2000/svg}text')]
            self.assertTrue(all(label in texts for label, _ in axes))

    def test_nonfinite_data_cannot_be_silently_drawn_as_full_strength(self):
        for value in (float('nan'), float('inf'), -float('inf')):
            with self.subTest(value=value), self.assertRaises(ValueError):
                render('Skills', [('A', value), ('B', 50), ('C', 20)], 'light', 440, 4, False, False)

    def test_invalid_chart_options_are_rejected_before_writing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'data.json'
            source.write_text('{"axes":[{"label":"A","value":1},{"label":"B","value":2},{"label":"C","value":3}]}')
            output = root / 'chart'
            for option, value in [('--size', '0'), ('--rings', '0'), ('--curve', 'nan'), ('--limit', '0')]:
                with self.subTest(option=option):
                    with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                        main(['--data', str(source), '--out', str(output), option, value])
                    self.assertEqual(error.exception.code, 2)
                    self.assertFalse(list(root.glob('chart-*.svg')))
