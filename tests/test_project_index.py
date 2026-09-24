import json
import tempfile
import unittest
from pathlib import Path

from scripts.project_index import load_projects, main, markdown, search_projects


class ProjectIndexTests(unittest.TestCase):
    def test_search_matches_all_words_across_fields_without_changing_order(self):
        projects = [{"repo": "One", "description": "Data drift", "technologies": ["Python"]},
                    {"repo": "Two", "description": "Web app", "technologies": ["Python"]}]
        self.assertEqual(search_projects(projects, " PYTHON drift "), [projects[0]])
        self.assertEqual(search_projects(projects, ""), projects)
        self.assertEqual(search_projects(projects, "rust"), [])

    def test_markdown_preserves_table_shape_and_escapes_html(self):
        result = markdown([{"repo": "example", "description": "a|b\n<img>", "technologies": []}])
        self.assertIn("a&#124;b &lt;img&gt;", result)
        self.assertIn("No matching projects.", markdown([]))

    def test_check_detects_stale_generated_content(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / "projects.json", Path(directory) / "index.md"
            source.write_text(json.dumps({"projects": [{"repo": "one", "description": "First"}]}))
            args = ["--projects", str(source), "--output", str(output)]
            self.assertEqual(main(args), 0)
            self.assertEqual(main([*args, "--check"]), 0)
            output.write_text("stale")
            self.assertEqual(main([*args, "--check"]), 1)
            source.write_text(json.dumps({"projects": [{"repo": "../bad", "description": "Bad"}]}))
            with self.assertRaises(ValueError):
                load_projects(source)
