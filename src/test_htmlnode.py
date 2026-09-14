import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    #Multiple props should each get a leading space and be joined together
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    #No props argument passed at all (defaults to None)/ empty string
    def test_props_to_html_none(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.props_to_html(), "")

    #Empty dict passed explicitly/ should still return empty string, not error
    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "This is a paragraph", None, {})
        self.assertEqual(node.props_to_html(), "")

    #Basic sanity check that constructor args are stored correctly
    def test_values(self):
        node = HTMLNode("div", "This is a div")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "This is a div")

    #Confirms the base class's to_html() intentionally isn't implemented
    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "This is a paragraph")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    #Confirms __repr__ formats all 4 fields in the right order
    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph", None, {"class": "text"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, This is a paragraph, None, {'class': 'text'})",
        )


if __name__ == "__main__":
    unittest.main()