import unittest

from text_parser import text_to_textnodes, markdown_to_blocks
from textnode import TextNode, TextType


class MyTestCase(unittest.TestCase):
    def test_something(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], text_to_textnodes(text))

    def test_code(self):
        text = "`This is **text** with an _italic_ word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)` should render as \nThis is **text** with an _italic_ word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual([
            TextNode("This is **text** with an _italic_ word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.CODE),
            TextNode(" should render as \nThis is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], text_to_textnodes(text))

    def test_nested_bold_italic(self):
        text = "this is _italic text_ with an underscore delimiter. This is **bold text** with a double star delimiter. This is **_bold italic text_**."
        self.assertEqual([
            TextNode("this is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" with an underscore delimiter. This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with a double star delimiter. This is ", TextType.TEXT),
            TextNode("bold italic text", TextType.BOLD_ITALIC),
            TextNode(".", TextType.TEXT),
        ], text_to_textnodes(text))

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
# Heading

## Subheading

Paragraph with text in it. 

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean suscipit diam id justo maximus euismod vel in lacus vitae orci. Duis congue, massa quis semper dapibus, mauris tellus fermentum odio, id bibendum massa ac arcu. Nullam nec tincidunt neque. Donec eget ipsum vel purus facilisis fermentum. Fusce nec lorem ac orci feugiat suscipit gravida eu eget odio. """
        blocks = markdown_to_blocks(md)
        self.assertEqual([
            "# Heading",
            "## Subheading",
            "Paragraph with text in it.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean suscipit diam id justo maximus euismod vel in lacus vitae orci. Duis congue, massa quis semper dapibus, mauris tellus fermentum odio, id bibendum massa ac arcu. Nullam nec tincidunt neque. Donec eget ipsum vel purus facilisis fermentum. Fusce nec lorem ac orci feugiat suscipit gravida eu eget odio."
        ], blocks)

if __name__ == '__main__':
    unittest.main()
