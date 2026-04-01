from .blocks import BlockType, markdown_to_blocks, block_to_block_type


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

def text_to_children(text):
    from .textnode import text_to_textnodes, text_node_to_html_node

    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def create_heading_node(block):
    from .parentnode import ParentNode

    stripped_hashes = block.lstrip("#")
    count = len(block) - len(stripped_hashes)
    tag = f"h{count}"
    return ParentNode(tag, text_to_children(stripped_hashes.strip()))

def create_paragraph_node(block):
    from .parentnode import ParentNode

    text = " ".join(line.strip() for line in block.split("\n"))
    return ParentNode("p", text_to_children(text))

def create_quote_node(block):
    from .parentnode import ParentNode

    lines = []
    for line in block.split("\n"):
        line = line[1:]  # remove '>'
        if line.startswith(" "):
            line = line[1:]
        lines.append(line)
    return ParentNode("blockquote", text_to_children(" ".join(lines)))

def create_list_node(block):
    from .parentnode import ParentNode

    items = []
    for line in block.split("\n"):
        _, item_text = line.split(". ", 1)
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)

def create_ulist_node(block):
    from .parentnode import ParentNode

    items = []
    for line in block.split("\n"):
        item_text = line[2:]  # "- "
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ul", items)

def create_code_node(block):
    from .leafnode import LeafNode
    from .parentnode import ParentNode

    code_text = "\n".join(block.split("\n")[1:-1])
    return ParentNode("pre", [LeafNode("code", code_text)])

def create_specific_html_node(block_type, block):
    match block_type:
        case BlockType.HEADING:
            return create_heading_node(block)
        case BlockType.PARAGRAPH:
            return create_paragraph_node(block)
        case BlockType.QUOTE:
            return create_quote_node(block)
        case BlockType.ORDERED_LIST:
            return create_list_node(block)
        case BlockType.UNORDERED_LIST:
            return create_ulist_node(block)
        case BlockType.CODE:
            return create_code_node(block)
        case _:
            raise ValueError("BlockType is undefined")

            

def markdown_to_html_node(markdown):
    from .parentnode import ParentNode
    from .blocks import markdown_to_blocks, block_to_block_type

    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(create_specific_html_node(block_type, block))
    return ParentNode("div", children)

