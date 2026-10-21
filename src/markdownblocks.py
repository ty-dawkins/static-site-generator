# Splits a full markdown document into blocks.
def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        # Trim leading/trailing whitespace and newlines from each block
        block = block.strip()
        # Skip empty blocks left behind by extra blank lines
        if block == "":
            continue
        blocks.append(block)
    return blocks