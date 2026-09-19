import unittest
from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    # Basic code-block split, matches the assignment example
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    # Bold delimiter, matches the assignment's intro example
    def test_split_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    # Italic delimiter
    def test_split_italic(self):
        node = TextNode("This is an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    # Multiple delimited sections in one string
    def test_split_multiple_occurrences(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code1", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
            ],
        )

    # Non-text nodes should pass through unchanged, untouched by splitting
    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    # No delimiter present at all: the whole text stays as one TEXT node
    def test_no_delimiter_present(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Just plain text", TextType.TEXT)])

    # Unclosed delimiter should raise, since it's invalid markdown
    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is text with a `unclosed code word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    # Delimited text at the very start of the string (empty leading section
    # should be dropped, not turned into an empty TextNode)
    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" at the start", TextType.TEXT),
            ],
        )

    # Multiple old_nodes in the input list should all be processed independently
    def test_multiple_input_nodes(self):
        node1 = TextNode("`code` here", TextType.TEXT)
        node2 = TextNode("more `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
                TextNode("more ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()