# Splits a full markdown document into blocks.
# Blocks are separated by a blank line, EXCEPT inside a ``` code block,
# where blank lines are part of the code and must be kept.
def markdown_to_blocks(markdown):
    blocks = []
    current = []      # lines of the block being built
    in_code = False   # are we between an opening and closing ```?

    for line in markdown.split("\n"):
        # An odd number of ``` on a line opens or closes a code block
        # (a line like ```inline``` has two, so it doesn't toggle)
        if line.count("```") % 2 == 1:
            in_code = not in_code

        # A blank line outside code ends the current block
        if line.strip() == "" and not in_code:
            add_block(blocks, current)
            current = []
        else:
            current.append(line)

    # Don't forget the last block
    add_block(blocks, current)
    return blocks


# Joins a block's lines, trims the outside, and skips it if empty
def add_block(blocks, lines):
    block = "\n".join(lines).strip()
    if block != "":
        blocks.append(block)