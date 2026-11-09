"""Regression tests for link targets that file-existence checks cannot validate."""

from pathlib import Path
import tempfile
import unittest

from markdown_links import check_local_links, markdown_anchors


class MarkdownLinkTests(unittest.TestCase):
    def check(self, files):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return check_local_links(root)

    def test_existing_file_with_renamed_heading_fails(self):
        errors = self.check({"index.md": "[metrics](scope.md#ten-dimensions)",
                             "scope.md": "## Research dimensions\n"})
        self.assertEqual(errors, [("index.md", 1, "scope.md#ten-dimensions", "anchor does not exist")])

    def test_same_file_and_cross_file_fragments(self):
        self.assertEqual(self.check({"index.md": "# Start\n[here](#start)\n[there](scope.md#research-dimensions)",
                                     "scope.md": "## Research dimensions\n"}), [])
        errors = self.check({"index.md": "# Start\n[bad](#missing)"})
        self.assertEqual(errors[0][1:], (2, "#missing", "anchor does not exist"))

    def test_encoded_unicode_paths_fragments_and_query(self):
        self.assertEqual(self.check({"index.md": "[text](<notes%20ru.md?raw=1#%D1%82%D0%B5%D1%81%D1%82>)",
                                     "notes ru.md": "# Тест\n"}), [])

    def test_duplicate_headings_and_slug_collisions(self):
        anchors = markdown_anchors("# Topic\n# Topic\n# Topic-1\n# Topic\n")
        self.assertEqual(anchors, {"topic", "topic-1", "topic-1-1", "topic-2"})

    def test_formatting_setext_and_explicit_html_anchors(self):
        anchors = markdown_anchors('## **Hello**, [world](other.md) & `code_id`! ##\n'
                                   'Setext heading\n==============\n<a id="custom"></a>\n<a name="old"></a>\n## _Emphasis_\n')
        self.assertEqual(anchors, {"hello-world--code_id", "setext-heading", "custom", "old", "emphasis"})
        self.assertEqual(self.check({"index.md": "[page](page.html#custom)",
                                     "page.html": '<h2 id="custom">Title</h2>'}), [])

    def test_code_and_comments_do_not_create_anchors_or_links(self):
        content = '# Real\n```md\n# Fake\n[bad](missing.md)\n```\n<!-- # Hidden -->\n`[bad](missing.md)`\n`<a id="fake-anchor"></a>`'
        self.assertEqual(markdown_anchors(content), {"real"})
        self.assertEqual(self.check({"index.md": content}), [])
        self.assertEqual(len(self.check({"index.md": content + '\n[bad](#fake)'})), 1)

    def test_reference_links_check_fragments(self):
        text = '# Present\n[good][ok]\n[bad][]\n[shortcut]\n\n[ok]: #present\n[bad]: #gone\n[shortcut]: #absent\n'
        errors = self.check({"index.md": text})
        self.assertEqual([(e[1], e[2]) for e in errors], [(3, '#gone'), (4, '#absent')])

    def test_external_schemes_are_skipped_and_missing_files_fail(self):
        self.assertEqual(self.check({"index.md": '[web](https://example.com/#absent) [mail](mailto:a@example.com) [web](//example.com/#absent)'}), [])
        self.assertEqual(self.check({"index.md": '[bad](missing.md#heading)'})[0][3], 'file does not exist')


if __name__ == "__main__":
    unittest.main()
