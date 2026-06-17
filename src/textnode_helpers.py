from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type in [TextType.TEXT]:
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