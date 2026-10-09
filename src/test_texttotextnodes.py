import unittest
from textnode import TextNode, TextType
from texttotextnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    # Every inline type in one string, matches the assignment example
    def test_all_types(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    # Plain text comes back as a single TEXT node
    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            text_to_textnodes("Just plain text"),
        )

    # Only bold
    def test_only_bold(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**"),
        )

    # Multiple of the same type
    def test_multiple_bold(self):
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
            text_to_textnodes("**one** and **two**"),
        )

    # Image and link side by side are split into the right types
    def test_image_and_link(self):
        self.assertListEqual(
            [
                TextNode("pic", TextType.IMAGE, "https://a.com/a.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes("![pic](https://a.com/a.png) [site](https://boot.dev)"),
        )

    # Unclosed delimiter still raises, coming up from split_nodes_delimiter
    def test_unclosed_bold_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **broken")


if __name__ == "__main__":
    unittest.main()
