from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images, extract_markdown_links


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Non-text nodes (bold, links, other images) pass through untouched
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining = old_node.text
        images = extract_markdown_images(remaining)
        # No images: keep the original node as-is
        if not images:
            new_nodes.append(old_node)
            continue

        for alt, url in images:
            # Split once around this image: [text before, text after]
            sections = remaining.split(f"![{alt}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown: image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            # Keep working on whatever comes after this image
            remaining = sections[1]

        # Any text left after the last image
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Non-text nodes (bold, images, other links) pass through untouched
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining = old_node.text
        links = extract_markdown_links(remaining)
        # No links: keep the original node as-is
        if not links:
            new_nodes.append(old_node)
            continue

        for anchor, url in links:
            # Split once around this link: [text before, text after]
            sections = remaining.split(f"[{anchor}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown: link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            # Keep working on whatever comes after this link
            remaining = sections[1]

        # Any text left after the last link
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes