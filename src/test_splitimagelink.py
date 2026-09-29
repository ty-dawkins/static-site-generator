import unittest
from textnode import TextNode, TextType
from splitimagelink import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):
    # Two images with text between
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    # No images: the original node comes back unchanged
    def test_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    # Image only: no empty text nodes before or after
    def test_image_only(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            split_nodes_image([node]),
        )

    # Image at the start with trailing text
    def test_image_at_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) after", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" after", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    # Two images back to back: no empty text node between them
    def test_adjacent_images(self):
        node = TextNode(
            "![a](https://a.com/a.png)![b](https://b.com/b.png)", TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://a.com/a.png"),
                TextNode("b", TextType.IMAGE, "https://b.com/b.png"),
            ],
            split_nodes_image([node]),
        )

    # Links are left alone by the image splitter
    def test_image_ignores_links(self):
        node = TextNode("A [link](https://www.boot.dev) here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    # Non-text nodes pass through untouched
    def test_image_non_text_passthrough(self):
        node = TextNode("bold", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))

    # Multiple input nodes are each processed, in order
    def test_image_multiple_nodes(self):
        nodes = [
            TextNode("first ![a](https://a.com/a.png)", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("no images", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("first ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://a.com/a.png"),
                TextNode("bold", TextType.BOLD),
                TextNode("no images", TextType.TEXT),
            ],
            split_nodes_image(nodes),
        )


class TestSplitNodesLink(unittest.TestCase):
    # Two links
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            split_nodes_link([node]),
        )

    # No links: the original node comes back unchanged
    def test_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    # Link with trailing text
    def test_link_with_trailing_text(self):
        node = TextNode("[boot dev](https://www.boot.dev) is great", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is great", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    # Images are left alone by the link splitter
    def test_link_ignores_images(self):
        node = TextNode("An ![image](https://i.imgur.com/zjjcJKZ.png) here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    # Mixed: only the link is split out, the image stays inside the text
    def test_link_with_image_in_text(self):
        node = TextNode(
            "![img](https://a.com/a.png) and [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("![img](https://a.com/a.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            split_nodes_link([node]),
        )

    # Non-text nodes pass through untouched
    def test_link_non_text_passthrough(self):
        node = TextNode("code", TextType.CODE)
        self.assertListEqual([node], split_nodes_link([node]))


if __name__ == "__main__":
    unittest.main()