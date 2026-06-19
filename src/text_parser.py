from blocks import block_to_html_node
from htmlnode import HTMLNode, ParentNode


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


