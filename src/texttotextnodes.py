from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter
from splitimagelink import split_nodes_image, split_nodes_link


def text_to_textnodes(text):
    # Start with the whole string as one plain TEXT node
    nodes = [TextNode(text, TextType.TEXT)]
    # Each splitter only breaks up TEXT nodes, so they can be chained
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
