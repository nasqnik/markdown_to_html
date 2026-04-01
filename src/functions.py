from .textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list.append(node)
            continue
        
        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Missing closing delimiter: {delimiter}")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                list.append(TextNode(part, TextType.TEXT))
            else:
                list.append(TextNode(part, text_type))

    return list

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for alt, url in matches:
            markdown = f"![{alt}]({url})"
            parts = text.split(markdown, 1)

            if len(parts) != 2:
                raise ValueError(f"Invalid markdown image: {markdown}")

            before, after = parts
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after 

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for anchor, url in matches:
            markdown = f"[{anchor}]({url})"
            parts = text.split(markdown, 1)

            if len(parts) != 2:
                raise ValueError(f"Invalid markdown link: {markdown}")

            before, after = parts
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = after 

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found")

