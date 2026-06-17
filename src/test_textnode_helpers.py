import unittest

from textnode import TextNode, TextType
from textnode_helpers import split_nodes_delimiter


class MyTestCase(unittest.TestCase):
    def test_something(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_something_else(self):
        node = TextNode("This is text ending with a **bold** **word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0], TextNode("This is text ending with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("word", TextType.BOLD))

    def test_nested_handled(self):
        node = TextNode("This is text with both **bold and _italics words_**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with both ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold and ", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode("italics words", TextType.ITALIC))

    def test_nested_ignored(self):
        node = TextNode("This is a code example: `this is markdown with **bold text**` and it shouldn't break up the markdown in the code example", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)


if __name__ == '__main__':
    unittest.main()
