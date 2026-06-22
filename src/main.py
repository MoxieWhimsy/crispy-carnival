from file_ops import clear_and_copy, generate_page, generate_page_recursive
from textnode import TextType, TextNode

clear_and_copy('static', 'public')
generate_page_recursive('content', 'template.html', 'public')