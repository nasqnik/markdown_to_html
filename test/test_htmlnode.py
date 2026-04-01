import unittest

from src.htmlnode import HTMLNode, markdown_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )
    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "hello", None, {})
        self.assertEqual(node.props_to_html(), "")
    def test_props_to_html_none(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.props_to_html(), "")
    def test_props_to_html_single_prop(self):
        node = HTMLNode("img", None, None, {"src": "logo.png"})
        self.assertEqual(node.props_to_html(), ' src="logo.png"')

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_heading_block(self):
        md = "# Main title"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h1>Main title</h1></div>")

    def test_quote_block(self):
        md = "> first line\n> second line"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><blockquote>first line second line</blockquote></div>")

    def test_unordered_list_block(self):
        md = "- one\n- two\n- three"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>")

    def test_ordered_list_block(self):
        md = "1. alpha\n2. beta"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><ol><li>alpha</li><li>beta</li></ol></div>")

    def test_image_and_link_inline(self):
        md = "A ![logo](https://img.dev/logo.png) and [site](https://boot.dev)"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>A <img src="https://img.dev/logo.png" alt="logo"></img> and <a href="https://boot.dev">site</a></p></div>',
        )

if __name__ == "__main__":
    unittest.main()