import os
import shutil
import sys

from .functions import extract_title
from .htmlnode import markdown_to_html_node


def copy_recursive(src_path, dst_path):
    if os.path.isfile(src_path):
        shutil.copy(src_path, dst_path)
        print(f"Copied file: {src_path} -> {dst_path}")
        return

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    for entry in os.listdir(src_path):
        src_child = os.path.join(src_path, entry)
        dst_child = os.path.join(dst_path, entry)
        copy_recursive(src_child, dst_child)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dst_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dst_path, basepath)
        elif os.path.isfile(src_path) and src_path.endswith(".md"):
            html_dest = os.path.splitext(dst_path)[0] + ".html"
            generate_page(src_path, template_path, html_dest, basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_content)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.startswith("/"):
        basepath = f"/{basepath}"
    if not basepath.endswith("/"):
        basepath = f"{basepath}/"

    project_root = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(project_root, "static")
    docs_dir = os.path.join(project_root, "docs")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    os.mkdir(docs_dir)

    copy_recursive(static_dir, docs_dir)
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)

if __name__ == "__main__":
    main()