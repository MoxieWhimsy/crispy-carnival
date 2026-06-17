import unittest

from blocks import BlockType, block_to_block_type


class MyTestCase(unittest.TestCase):
    def test_code_block(self):
        text = """```
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(str.strip, blocks))
    return blocks
        ```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_quote_block(self):
        text = """> This is a quote"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_paragraph_block(self):
        text = """This is a paragraph. Trapped in the Moon. """
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_heading_block(self):
        text = """### Heading """
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_unordered_block(self):
        text = """* the items in this list are unordered
* item
* item"""
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED)

    def test_ordered_block(self):
        text = """1. the items 
2. in this list
3. are ordered"""
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED)


if __name__ == '__main__':
    unittest.main()
