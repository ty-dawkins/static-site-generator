from textnode import TextNode, TextType, text_node_to_html_node
from texttotextnodes import text_to_textnodes
from markdownblocks import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from parentnode import ParentNode


# Converts a full markdown document into one <div> ParentNode
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)


# Picks the right converter for a block based on its type
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    raise ValueError(f"Invalid block type: {block_type}")


# Shared helper: inline markdown text -> list of HTMLNodes
# (text -> TextNodes -> LeafNodes)
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


# <p>: lines are joined with spaces into one paragraph
def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


# <h1>-<h6>: count the "#"s, then drop them and the space
def heading_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


# <pre><code>: no inline parsing, text stays exactly as written
def code_to_html_node(block):
    # Drop the opening ```\n (4 chars) and closing ``` (3 chars)
    text = block[4:-3]
    code = text_node_to_html_node(TextNode(text, TextType.TEXT))
    return ParentNode("pre", [ParentNode("code", [code])])


# <blockquote>: strip ">" and the optional space from each line
def quote_to_html_node(block):
    new_lines = []
    for line in block.split("\n"):
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(text))


# <ul> with an <li> per line; drop the "- " from each line
def ulist_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


# <ol> with an <li> per line; drop the "1. ", "2. ", etc.
def olist_to_html_node(block):
    items = []
    for line in block.split("\n"):
        # Everything after the first ". " is the item text
        text = line.split(". ", 1)[1]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)