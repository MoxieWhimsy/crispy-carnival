from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(text_block: str) -> BlockType:
    if text_block.startswith("#"):
        return BlockType.HEADING
    if text_block.startswith("```") and text_block.endswith("```"):
        return BlockType.CODE
    if text_block.startswith(">"):
        return BlockType.QUOTE
    if text_block.startswith("* ") or text_block.startswith("- ") or text_block.startswith("+ "):
        return BlockType.UNORDERED
    if len(re.findall(r"^\d+\.\s", text_block)) > 0:
        return BlockType.ORDERED

    return BlockType.PARAGRAPH
