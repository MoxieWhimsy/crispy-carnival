import unittest

from htmlnode import HTMLNode
from text_parser import markdown_to_html_node, markdown_to_blocks
from textnode import TextNode, TextType
from textnode_helpers import text_to_textnodes


class MyTestCase(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

        node: HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_something(self):
        self.maxDiff = None
        md = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        th = '<div><p>This is <b>text</b> with an <i>italic</i> word and a <code>code block</code> and an <img src="https://i.imgur.com/fJRm4Vk.jpeg" alt="obi wan image"></img> and a <a href="https://boot.dev">link</a></p></div>'
        node: HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            th
        )

    def test_nested_bold_italic(self):
        md = "this is _italic text_ with an underscore delimiter. This is **bold text** with a double star delimiter. This is **_bold italic text_**."
        th = '<div><p>this is <i>italic text</i> with an underscore delimiter. This is <b>bold text</b> with a double star delimiter. This is <b><i>bold italic text</i></b></p></div>.'
        node: HTMLNode = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), th)

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

    def test_markdown_to_blocks_3(self):
        self.maxDiff = None
        md = """
# Heading

Paragraph with text in it. 

- List item
- List item

> My humanitarian work evolved from being with my family. My mom, my dad, they really set a great example for giving
> back. My mom was a nurse, my dad was a school teacher. But my mom did a lot of things for geriatrics and elderly
> people. She would do home visits for free.
> ~ Cat Cora
        """
        th = ('<div><h1>Heading</h1><p>Paragraph with text in it.</p><ul><li>List item</li><li>List item</li></ul>'
              '<blockquote>My humanitarian work evolved from being with my family. My mom, my dad, they really set a '
              'great example for giving back. My mom was a nurse, my dad was a school teacher. But my mom did a lot '
              'of things for geriatrics and elderly people. She would do home visits for free. ~ Cat Cora</blockquote></div>')
        node: HTMLNode = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), th)

if __name__ == '__main__':
    unittest.main()
