from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # Non-text nodes (already bold, italic, etc.) pass through untouched
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)
        # An even number of sections means an odd number of delimiters,
        # which means a delimiter was opened but never closed
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: no closing delimiter found for '{delimiter}'"
            )

        for i, section in enumerate(sections):
            if section == "":
                continue
            # Even indices are plain text (outside delimiters),
            # odd indices are the delimited text_type content
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes