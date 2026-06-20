from file_ops import clear_and_copy
from textnode import TextType, TextNode

clear_and_copy('static', 'public')
print("hello world")

dummy = TextNode("This is a dummy node", TextType.LINK, "https://www.boot.dev")
print(dummy)