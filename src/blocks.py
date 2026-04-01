from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):

    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING
    
    if re.match(r"^```[\s\S]*```$", block):
        return BlockType.CODE
    
    lines = block.split("\n")

    if all(re.match(r"^> ?.*$", line) for line in lines):
        return BlockType.QUOTE

    if all(re.match(r"^- .+$", line) for line in lines):
        return BlockType.UNORDERED_LIST        
    
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        clean_blocks.append(block)
    return clean_blocks