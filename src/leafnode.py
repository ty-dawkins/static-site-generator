from htmlnode import HTMLNode

# LeafNode represents a leaf node in the HTML tree, which has no children and contains a value (text content).
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    # Converts the LeafNode to its HTML representation.
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    #no children 
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"