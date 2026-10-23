import unittest
from markdowntohtml import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    # Two paragraphs with inline markdown; newlines become spaces
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # Code block keeps inline markdown as raw text
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    # Heading levels map to h1-h6, inline markdown still works
    def test_headings(self):
        md = """
# Heading one

### Heading **three**

###### Heading six
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading one</h1><h3>Heading <b>three</b></h3><h6>Heading six</h6></div>",
        )

    # Quote lines are joined, ">" and optional space removed
    def test_quote(self):
        md = """
> This is a
>quote with _italic_
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <i>italic</i></blockquote></div>",
        )

    # Unordered list: <ul> with an <li> per item
    def test_unordered_list(self):
        md = """
- first item
- **bold** item
- item with `code`
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li><b>bold</b> item</li><li>item with <code>code</code></li></ul></div>",
        )

    # Ordered list: <ol> with an <li> per item
    def test_ordered_list(self):
        md = """
1. first
2. _second_
3. third
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li><i>second</i></li><li>third</li></ol></div>",
        )

    # Links and images inside a paragraph
    def test_link_and_image(self):
        md = "A [link](https://boot.dev) and ![pic](https://a.com/a.png)"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><p>A <a href="https://boot.dev">link</a> and <img src="https://a.com/a.png" alt="pic"></img></p></div>',
        )

    # Every block type in one document, in order
    def test_mixed_document(self):
        md = """
# Title

Some **intro** text.

> A quote

- one
- two

1. first
2. second

```
code here
```
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>Some <b>intro</b> text.</p><blockquote>A quote</blockquote><ul><li>one</li><li>two</li></ul><ol><li>first</li><li>second</li></ol><pre><code>code here\n</code></pre></div>",
        )


    # Empty document: just an empty <div>, no crash
    def test_empty_document(self):
        self.assertEqual(markdown_to_html_node("").to_html(), "<div></div>")

    # Extra blank lines don't create empty <p></p> nodes
    def test_extra_blank_lines(self):
        md = "\n\n\n# Title\n\n\n\n\nSome text\n\n\n"
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h1>Title</h1><p>Some text</p></div>",
        )

    # Code block keeps blank lines and indentation exactly
    def test_codeblock_blank_lines_and_indentation(self):
        md = """
```
def f():
    x = 1

    return x
```
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><pre><code>def f():\n    x = 1\n\n    return x\n</code></pre></div>",
        )

    # 10+ items: "10. " is 4 chars, so a fixed [3:] slice would break here
    def test_ordered_list_ten_plus_items(self):
        md = "\n".join(f"{i}. item {i}" for i in range(1, 12))
        expected = "".join(f"<li>item {i}</li>" for i in range(1, 12))
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            f"<div><ol>{expected}</ol></div>",
        )

if __name__ == "__main__":
    unittest.main()