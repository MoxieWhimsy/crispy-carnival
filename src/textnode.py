from enum import Enum

from htmlnode import LeafNode, HTMLNode, ParentNode


class TextType(Enum):
    TEXT = {"text/plain"}
    BOLD_ITALIC = {"text/bold", "text/italic"}
    BOLD = {"text/bold"}
    ITALIC = {"text/italic"}
    CODE = {"code"}
    LINK = {"link"}
    IMAGE = {"image"}

    def __str__(self) -> str:
        return f'"{" ".join(self.value)}"'

    def __contains__(self, item):
        for part in item.value:
            if part not in self.value:
                return False
        return True

    def __add__(self, other):
        if not isinstance(other, TextType):
            raise TypeError(f"Cannot add {type(other)} with {type(TextType)}")

        if self == TextType.TEXT:
            return other
        if other == TextType.TEXT:
            return self

        return TextType(value=self.value.union(other.value))

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.BOLD_ITALIC:
            return ParentNode("b", [LeafNode("i", text_node.text)])
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            url = text_node.url if text_node.url else ""
            return LeafNode("a", text_node.text, {"href": url})
        case TextType.IMAGE:
            source = text_node.url if text_node.url else ""
            alt_text = text_node.text if text_node.text else ""
            return LeafNode("img", "", {"src": source, "alt": alt_text})
        case _:
            return LeafNode(None, "")
