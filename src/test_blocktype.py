import unittest
from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    # Headings: 1 through 6 "#" followed by a space
    def test_heading_levels(self):
        for i in range(1, 7):
            block = "#" * i + " Heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    # 7 "#" is too many, so it's just a paragraph
    def test_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    # "#" with no space after it is not a heading
    def test_heading_needs_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # Code: ``` + newline at the start, ``` at the end
    def test_code(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # Code with no newline after the opening ``` is not a code block
    def test_code_needs_newline(self):
        self.assertEqual(block_to_block_type("```print('hi')```"), BlockType.PARAGRAPH)

    # Code that never closes is not a code block
    def test_code_unclosed(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')"), BlockType.PARAGRAPH)

    # Quote: every line starts with ">", space optional
    def test_quote(self):
        block = "> line one\n>line two\n> line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    # One line missing ">" breaks the quote
    def test_quote_missing_marker(self):
        block = "> line one\nline two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Unordered list: every line starts with "- "
    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    # "-" with no space after it is not a list item
    def test_unordered_list_needs_space(self):
        block = "- one\n-two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Ordered list: 1. 2. 3. counting up by 1
    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # Ordered list must start at 1
    def test_ordered_list_must_start_at_one(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Ordered list can't skip a number
    def test_ordered_list_skips_number(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Ordered list needs a space after the "."
    def test_ordered_list_needs_space(self):
        block = "1.one\n2.two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Ordered list past 9 still counts correctly (10. 11. ...)
    def test_ordered_list_double_digits(self):
        block = "\n".join(f"{i}. item" for i in range(1, 12))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # Plain text is a paragraph
    def test_paragraph(self):
        block = "Just a normal paragraph\nwith two lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()