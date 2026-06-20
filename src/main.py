from file_ops import clear_and_copy, generate_page
from textnode import TextType, TextNode

clear_and_copy('static', 'public')
generate_page('content/index.md', 'template.html', 'public/index.html')

print("hello world")

dummy = TextNode("This is a dummy node", TextType.LINK, "https://www.boot.dev")
print(dummy)