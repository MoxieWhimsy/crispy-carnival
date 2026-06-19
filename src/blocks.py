import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from text_helpers import strip_front_char
from textnode import TextNode, TextType
from textnode_helpers import text_to_html_inline, text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(text_block: str) -> BlockType:
    if text_block.startswith("#") and not text_block.endswith("#"):
        block = text_block
        count: int = 0
        while block.startswith("#"):
            count += 1
            block = block[1:]
        if count <= 6:
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

def block_to_html_node(block: str) -> HTMLNode | None:
    def convert_inline_li(line: str) -> HTMLNode:
        return text_to_html_inline(line, "li")

    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.CODE:
            first_line_return = block.find("\n")
            block = block[first_line_return+1:-3] # remove first line (with ```) and trailing ```
            node = TextNode(block, TextType.CODE)
            return ParentNode("pre", [text_node_to_html_node(node)])
        case BlockType.HEADING:
            count: int = 0
            while block.startswith("#"):
                count += 1
                block = block[1:]
            block = block.lstrip()
            return text_to_html_inline(block, f"h{count}")
        case BlockType.ORDERED:
            lines = block.split("\n")
            items: list[HTMLNode] = list(map(convert_inline_li, lines))
            return ParentNode("ol", items)
        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            block = ' '.join(lines)
            nodes: list[TextNode] = text_to_textnodes(block)
            items: list[HTMLNode] = list(map(text_node_to_html_node, nodes))
            return ParentNode("p", items)
        case BlockType.QUOTE:
            lines = block.split("\n")
            accumulator: list[str] = list(map(strip_front_char, lines))
            nodes = text_to_textnodes(" ".join(accumulator))
            items: list[HTMLNode] = list(map(text_node_to_html_node, nodes))

            if len(lines) == 1:
                return ParentNode("q", items)

            return ParentNode("blockquote", items)
        case BlockType.UNORDERED:
            lines = list(map(strip_front_char, block.split("\n")))
            items: list[HTMLNode] = list(map(convert_inline_li, lines))
            return ParentNode("ul", items)
        case _:
            raise NotImplementedError(f'block type {block_type} not implemented')