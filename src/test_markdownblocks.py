import unittest
from markdownblocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    # Matches the assignment example
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # Heading, paragraph, and list: the lesson's intro example
    def test_heading_paragraph_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    # Extra blank lines between blocks should not create empty blocks
    def test_excessive_newlines(self):
        md = """First block



Second block"""
        self.assertEqual(markdown_to_blocks(md), ["First block", "Second block"])

    # Leading/trailing spaces on a block get stripped
    def test_strips_whitespace(self):
        md = "   padded block   \n\n  another  "
        self.assertEqual(markdown_to_blocks(md), ["padded block", "another"])

    # A single block with no blank lines comes back as one item
    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("Just one block"), ["Just one block"])

    # Empty or whitespace/only input returns an empty list
    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("\n\n\n   \n\n"), [])


    # A code block with a blank line inside stays ONE block
    def test_code_block_with_blank_line(self):
        md = """Intro

```
def f():
    x = 1

    return x
```

Outro"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Intro",
                "```\ndef f():\n    x = 1\n\n    return x\n```",
                "Outro",
            ],
        )

    # A "blank" line that only has spaces still separates blocks
    def test_whitespace_only_separator(self):
        self.assertEqual(markdown_to_blocks("a\n   \nb"), ["a", "b"])

if __name__ == "__main__":
    unittest.main()