from textnode import TextNode, TextType
from textnode_helpers import split_nodes_delimiter, split_nodes_image, split_nodes_link


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(str.strip, blocks))
    return blocks

def text_to_textnodes(text: str) -> list[TextNode]:
    original_node = TextNode(text, TextType.TEXT)
    nodes = [original_node]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "***", TextType.BOLD_ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes