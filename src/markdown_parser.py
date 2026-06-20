from blocks import block_to_html_node, block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode
from text_helpers import get_header_level
from textnode import TextNode
from textnode_helpers import text_to_textnodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(str.strip, blocks))
    blocks = list(filter(None, blocks))
    return blocks

def markdown_to_html_node(markdown: str) -> HTMLNode:
    result: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node = block_to_html_node(block)
        if node is None:
            print(f'warning: failed to process block {block}')
            continue
        result.append(node)
    return ParentNode("div", result)

def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if 1 == get_header_level(block):
                node = block_to_html_node(block)
                if node is None or node.value is None or node.tag != 'h1':
                    continue
                return node.value
    raise Exception(f"failed to extract title from markdown: {markdown}")
