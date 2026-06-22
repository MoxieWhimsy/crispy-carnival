import os
import shutil

from markdown_parser import markdown_to_html_node, extract_title


def clear_and_copy(source: str, destination: str):
    if not os.path.isdir(source):
        raise TypeError("Source must be a directory")
    shutil.rmtree(destination, ignore_errors=True)
    os.mkdir(destination)
    contents = os.listdir(source)
    if contents is None or len(contents) == 0:
        return
    directories = filter(lambda x: os.path.isdir(os.path.join(source, x)), contents)
    files = filter(lambda x: os.path.isfile(os.path.join(source, x)), contents)
    for directory in directories:
        directory_path = os.path.join(destination, directory)
        clear_and_copy(os.path.join(source, directory), directory_path)
    for file in files:
        shutil.copy(os.path.join(source, file), destination)

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.isfile(from_path):
        raise TypeError("from_path must be a file")
    if not os.path.isfile(template_path):
        raise TypeError("template must be a file")
    file = open(from_path, "r")
    template_file = open(template_path, "r")
    template = template_file.read()
    content = file.read()
    file.close()
    template_file.close()
    content_html_node = markdown_to_html_node(content)
    content_html = content_html_node.to_html()
    title = extract_title(content)
    full_html = template.replace("{{ Content }}", content_html).replace("{{ Title }}", title)
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if not os.path.isdir(dir_path_content):
        raise TypeError("content path must be a directory")
    if not os.path.isdir(dest_dir_path):
        os.mkdir(dest_dir_path)
    contents = os.listdir(dir_path_content)
    if contents is None or len(contents) == 0:
        return
    for content in contents:
        content_path = os.path.join(dir_path_content, content)
        target_path = os.path.join(dest_dir_path, content)
        if os.path.isdir(content_path):
            generate_page_recursive(content_path, template_path, target_path)
            continue
        if not os.path.isfile(content_path):
            continue
        if not content.endswith(".md"):
            continue

        target_path = target_path[:-2] + "html"
        generate_page(content_path, template_path, target_path)
