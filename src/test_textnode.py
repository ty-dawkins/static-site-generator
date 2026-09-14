import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # two nodes with the same text, type, and url should be equal
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # ommiting url should default to None, and two nodes should be equal
    def test_eq_url_none(self):
        node = TextNode("This is a text node", TextType.TEXT, None)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    # two nodes with the same text and type but different urls should not be equal
    def test_eq_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    #Different text content should not make nodes equal
    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    #same text but different text_type should make nodes not equal
    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    #same text/type but different url should make nodes not equal
    def test_not_eq_different_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    #a set url vs. a missing url should make nodes unequal 
    def test_not_eq_url_vs_none(self):
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK)
        self.assertNotEqual(node, node2)

    #repr() should format as TextNode(text, text_type_value, url)
    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(
            repr(node),
            "TextNode(This is some anchor text, link, https://www.boot.dev)",
        )


if __name__ == "__main__":
    unittest.main()