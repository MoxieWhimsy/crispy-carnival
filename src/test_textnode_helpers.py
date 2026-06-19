import unittest

from textnode import TextNode, TextType
from textnode_helpers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, \
    split_nodes_link, text_to_textnodes


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

    def test_something_else_entirely(self):
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

    def test_nested_handled(self):
        node = TextNode("This is text with both **bold and _italics words_**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with both ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold and ", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode("italics words", TextType.BOLD_ITALIC))

    def test_nested_ignored(self):
        node = TextNode("This is a code example: `this is markdown with **bold text**` and it shouldn't break up the markdown in the code example", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)

    def test_image_detection(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0][0], "rick roll")
        self.assertEqual(matches[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(matches[1][0], "obi wan")
        self.assertEqual(matches[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0][0], "to boot dev")
        self.assertEqual(matches[0][1], "https://www.boot.dev")
        self.assertEqual(matches[1][0], "to youtube")
        self.assertEqual(matches[1][1], "https://www.youtube.com/@bootdotdev")

    def test_extract_markdown_mailto_link(self):
        text = "This is text with a mailto link [Contact Us](mailto:contact@yourwebsite.com) as an example"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "Contact Us")
        self.assertEqual(matches[0][1], "mailto:contact@yourwebsite.com")

    def test_extract_markdown_mailto_link_complex(self):
        text = "This is text with a mailto link [Contact Support](mailto:contact@yourwebsite.com?subject='Support%20Request'&body='I%20need%20help%20with...') as an example"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "Contact Support")
        self.assertEqual(matches[0][1], "mailto:contact@yourwebsite.com?subject='Support%20Request'&body='I%20need%20help%20with...'")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_frontload(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) \n\n did you enjoy that?", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" \n\n did you enjoy that?", TextType.TEXT),
        ], new_nodes)

    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ], new_nodes)

    def test_split_mailto_link_complex(self):
        node = TextNode("This is text with a mailto link [Contact Support](mailto:contact@yourwebsite.com?subject='Support%20Request'&body='I%20need%20help%20with...') as an example", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a mailto link ", TextType.TEXT),
            TextNode("Contact Support", TextType.LINK, "mailto:contact@yourwebsite.com?subject='Support%20Request'&body='I%20need%20help%20with...'"),
            TextNode(" as an example", TextType.TEXT),
        ], new_nodes)


if __name__ == '__main__':
    unittest.main()
