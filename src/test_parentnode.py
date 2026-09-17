import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    # One level of nesting, single child
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    # Two levels of nesting: parent, then a child that is also a ParentNode, then a grandchild
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # Mix of tagged and raw-text LeafNode children, matching the assignment example
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    # No tag: should raise, since there's nothing to wrap children in
    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        with self.assertRaises(ValueError):
            node.to_html()

    # No children: should raise, since a parent with nothing inside is invalid
    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # Props on a parent node should render just like they do on a leaf
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    # Deeper nesting: parent, parent, parent, leaf, to stress the recursion
    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [ParentNode("p", [LeafNode("b", "deep text")])],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p><b>deep text</b></p></section></div>",
        )

    # Multiple ParentNode children side by side under one parent
    def test_to_html_multiple_parent_children(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode(None, "First")]),
                ParentNode("p", [LeafNode(None, "Second")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>First</p><p>Second</p></div>",
        )


if __name__ == "__main__":
    unittest.main()