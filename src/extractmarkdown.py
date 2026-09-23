import re
 
 
# Returns a list of (alt_text, url) tuples for every markdown image
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
 
 
# Returns a list of (anchor_text, url) tuples for every markdown link
# The (?<!!) lookbehind skips matches preceded by "!", so images aren't counted as links
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
 