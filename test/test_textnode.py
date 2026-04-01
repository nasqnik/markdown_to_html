import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes
from src.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_different_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node1, node2)

    def test_eq_with_default_url_none(self):
        node1 = TextNode("No URL here", TextType.TEXT)
        node2 = TextNode("No URL here", TextType.TEXT, None)
        self.assertEqual(node1, node2)

    def test_not_eq_none_url_vs_real_url(self):
        node1 = TextNode("A link", TextType.LINK)
        node2 = TextNode("A link", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    def test_not_eq_against_non_textnode(self):
        node = TextNode("Just text", TextType.TEXT)
        self.assertNotEqual(node, "Just text")

    def test_eq_empty_text(self):
        node1 = TextNode("", TextType.TEXT)
        node2 = TextNode("", TextType.TEXT, None)
        self.assertEqual(node1, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_node(self):
        node = TextNode("text", TextType.TEXT)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, None)
        self.assertEqual(html.value, "text")
        self.assertEqual(html.props, None)

    def test_bold_text_to_html_node(self):
        node = TextNode("bold text", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<b>bold text</b>")

    def test_italic_text_to_html_node(self):
        node = TextNode("italic text", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<i>italic text</i>")
        
    def test_code_text_to_html_node(self):
        node = TextNode("x = 1", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<code>x = 1</code>")

    def test_link_text_to_html_node(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), '<a href="https://example.com">Click me</a>')

    def test_image_text_to_html_node(self):
        node = TextNode("logo alt", TextType.IMAGE, "https://example.com/logo.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), '<img src="https://example.com/logo.png" alt="logo alt"></img>')
        
    def test_text_node_to_html_node_invalid_type_raises(self):
        node = TextNode("oops", "not-a-text-type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
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
            ],
            result,
        )

    def test_text_to_textnodes_plain_text_only(self):
        result = text_to_textnodes("just plain text")
        self.assertListEqual([TextNode("just plain text", TextType.TEXT)], result)

    def test_text_to_textnodes_multiple_same_type(self):
        result = text_to_textnodes("**one** and **two**")
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
            result,
        )

    def test_text_to_textnodes_image_and_link(self):
        result = text_to_textnodes(
            "img ![alt](https://img.com/a.png) then [site](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("img ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://img.com/a.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://boot.dev"),
            ],
            result,
        )

    def test_text_to_textnodes_raises_on_unclosed_delimiter(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is `broken")

if __name__ == "__main__":
    unittest.main()