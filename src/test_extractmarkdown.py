import unittest
from extractmarkdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    # Single image test
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    # Multiple images in one string, returned in order
    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    # No images present should return an empty list
    def test_no_images(self):
        matches = extract_markdown_images("Just plain text, no images here")
        self.assertListEqual([], matches)

    # Empty alt text is still a valid image
    def test_image_empty_alt(self):
        matches = extract_markdown_images("![](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    # A regular link should NOT be picked up as an image
    def test_images_ignores_links(self):
        matches = extract_markdown_images("A [link](https://www.boot.dev) only")
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    # Single link check
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    # Multiple links check
    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    # No links present should return an empty list
    def test_no_links(self):
        matches = extract_markdown_links("Just plain text, no links here")
        self.assertListEqual([], matches)

    # An image should NOT be picked up as a link (the lookbehind's job)
    def test_links_ignores_images(self):
        matches = extract_markdown_links("An ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

    # only the link comes back, not the image with mixed content
    def test_links_mixed_with_images(self):
        matches = extract_markdown_links(
            "![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)


if __name__ == "__main__":
    unittest.main()