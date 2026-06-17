import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_node(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    def test_props_to_html(self):
        node = HTMLNode(props={"test": "test"})
        self.assertEqual(node.props_to_html(), ' test="test"')

    def test_repr(self):
        node = HTMLNode(children=[HTMLNode(tag="span")])
        self.assertEqual(node.__repr__(), "tag: None, value: None, children: [tag: span, value: None, children: None, props: None], props: None")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_h2(self):
        node = LeafNode("h2", "This is a heading")
        self.assertEqual(node.to_html(), '<h2>This is a heading</h2>')

    def test_parent_node_p(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == '__main__':
    unittest.main()
