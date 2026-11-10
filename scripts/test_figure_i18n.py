"""Regression tests for language selection without corrupting charts or links."""

from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

from figure_i18n import cli_language, localized_path, save, translate


class FigureLanguageTests(unittest.TestCase):
    def test_cli_defaults_and_explicit_language(self):
        with patch("sys.argv", ["build_figures.py"]):
            self.assertEqual(cli_language(), "en")
        with patch("sys.argv", ["build_figures.py", "--lang", "ru"]):
            self.assertEqual(cli_language(), "ru")
        with self.assertRaises(ValueError):
            localized_path("figure.svg", "de")

    def test_svg_changes_text_but_preserves_numeric_geometry(self):
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650">'
               '<text x="88.5" y="3.36">88.5%</text>'
               '<text x="0" y="30">15 min/day</text>'
               '<circle cx="88.5" cy="426.0" data-value="88.5"/></svg>')
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"reach.svg"
            save(path, svg)
            translated = save(path, svg, "ru")
            self.assertEqual(path.read_text(), svg.replace('<svg ', '<svg xml:lang="en" ', 1))
            tree = ET.parse(translated).getroot()
            ns = "{http://www.w3.org/2000/svg}"
            self.assertEqual([e.text for e in tree.findall(ns+"text")], ["88,5%", "15 мин/день"])
            self.assertEqual(tree.find(ns+"circle").attrib, {"cx":"88.5", "cy":"426.0", "data-value":"88.5"})

    def test_html_language_links_and_style(self):
        page = ('<html lang="en"><style>.grid{width:88.5%}</style>'
                '<h1>Reach and consumption time</h1>'
                '<img src="gwi/reach.svg" alt="Weekly media reach">'
                '<a href="gwi/reach.txt">Annotation (TXT)</a>'
                '<a href="../data/media_use_2026.md">Source table</a></html>')
        with tempfile.TemporaryDirectory() as temp:
            result = save(Path(temp)/"index.html", page, "ru").read_text()
            self.assertIn('<html lang="ru">', result)
            self.assertIn('gwi/reach-ru.svg', result)
            self.assertIn('gwi/reach-ru.txt', result)
            self.assertIn('../data/media_use_2026.md', result)
            self.assertIn('.grid{width:88.5%}', result)
            self.assertIn('Пояснения (текстовый файл)', result)

    def test_native_russian_and_idempotent_paths(self):
        self.assertEqual(translate("Минут в неделю · подписи Ч:ММ", "en", "ru"),
                         "Minutes per week · HH:MM labels")
        self.assertEqual(localized_path("gwi/reach-ru.svg", "ru"), Path("gwi/reach-ru.svg"))
        self.assertEqual(translate("radar-overview.txt", "ru"), "radar-overview.txt")


if __name__ == "__main__":
    unittest.main()
