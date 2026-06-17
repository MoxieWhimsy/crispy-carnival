import re

from textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([\w\s]+)]\(([\w.:/]+)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"\[([\w\s]+)]\(([\w.:/@?&=%']+)\)", text)
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
                if index % 2 == 1:
                    result.append(TextNode(text, text_type))
                elif len(text) > 0:
                    result.append(TextNode(potential_split[index], node.text_type))
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
