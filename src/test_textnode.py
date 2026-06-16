import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is an image", TextType.IMAGE, "images/smiley.jpeg")
        node2 = TextNode("This is a link to an image", TextType.LINK, "images/smiley.jpeg")
        node3 = TextNode("This is a link to an image", TextType.IMAGE, "images/smiley.jpeg")
        node4 = TextNode("This is a link to an image", TextType.IMAGE)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node4)

    def test_str(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node), "TextNode(This is a text node, TextType.BOLD, None)")

if __name__ == '__main__':
    unittest.main()
