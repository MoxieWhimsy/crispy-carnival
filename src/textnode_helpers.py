import re

from htmlnode import LeafNode, HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def drop_empty_nodes(old_nodes: list[TextNode]) -> list[TextNode]:
    return [node for node in old_nodes if node.text is not None and len(node.text) > 0]

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^[\]]+?)]\(([^\s[\]()]+?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?:[^!]|^)\[([^[\]]+?)]\(([^\s[\]()]+?)\)", text)
    return matches

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type in [TextType.TEXT, TextType.BOLD, TextType.ITALIC]:
            potential_split = node.text.split(delimiter)
            if len(potential_split) % 2 == 0:
                raise Exception(f"non-matching delimiter detected: {delimiter}")
            for index in range(len(potential_split)):
                text = potential_split[index]
                if len(text) <= 0:
                    continue
                if index % 2 == 0:
                    result.append(TextNode(potential_split[index], node.text_type))
                    continue
                combined = text_type + node.text_type

                if TextType.BOLD_ITALIC in combined:
                    result.append(TextNode(potential_split[index], TextType.BOLD_ITALIC))
                    continue

                result.append(TextNode(text, text_type))


            continue
        # else
        result.append(node)
    return result

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if len(matches) <= 0:
            result.append(node)
            continue
        remaining_text = node.text
        for match in matches:
            alt_text, source = match
            sections = remaining_text.split(f'![{alt_text}]({source})', 1)
            if len(sections[0]) > 0:
                result.append(TextNode(sections[0], TextType.TEXT))
            remaining_text = sections[1] if len(sections) > 1 else ""
            result.append(TextNode(alt_text, TextType.IMAGE, source))
        if len(remaining_text) > 0:
            result.append(TextNode(remaining_text, TextType.TEXT))

    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if len(matches) <= 0:
            result.append(node)
            continue
        remaining_text = node.text
        for match in matches:
            link_text, link_url = match
            sections = remaining_text.split(f'[{link_text}]({link_url})', 1)
            if len(sections[0]) > 0:
                result.append(TextNode(sections[0], TextType.TEXT))
            remaining_text = sections[1] if len(sections) > 1 else ""
            result.append(TextNode(link_text, TextType.LINK, link_url))
        if len(remaining_text) > 0:
            result.append(TextNode(remaining_text, TextType.TEXT))

    return result


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
    # nodes = drop_empty_nodes(nodes)

    return nodes

def text_to_html_inline(line: str, tag: str) -> HTMLNode:
    nodes = text_to_textnodes(line)
    if len(nodes) == 1 and nodes[0].text_type == TextType.TEXT:
        return LeafNode(tag, nodes[0].text)
    sub_items: list[HTMLNode] = list(map(text_node_to_html_node, nodes))
    return ParentNode(tag, sub_items)

def text_to_html_nodes(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    if len(nodes) == 1 and nodes[0].text_type == TextType.TEXT:
        return [text_node_to_html_node(nodes[0])]
    sub_items: list[HTMLNode] = []
    for node in nodes:
        sub_items.append(text_node_to_html_node(node))
    return sub_items