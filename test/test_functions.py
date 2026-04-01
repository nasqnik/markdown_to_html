import unittest

from src.functions import *
from src.textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_bold_delimiter(self):
        node = TextNode("This has **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_italic_delimiter(self):
        node = TextNode("This has _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimited_sections(self):
        node = TextNode("a `b` c `d` e", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_non_text_nodes_are_untouched(self):
        nodes = [
            TextNode("plain", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("plain", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_missing_closing_delimiter_raises(self):
        node = TextNode("This is `broken markdown", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

class TestExtractFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](https://a.com/1.png) and ![two](https://a.com/2.png)"
        )
        self.assertListEqual(
            [("one", "https://a.com/1.png"), ("two", "https://a.com/2.png")],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("no images here")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[a](https://a.com) middle [b](https://b.com)"
        )
        self.assertListEqual(
            [("a", "https://a.com"), ("b", "https://b.com")],
            matches,
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("no links here")
        self.assertListEqual([], matches)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("plain text only", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([TextNode("plain text only", TextType.TEXT)], result)

    def test_split_nodes_delimiter_empty_input(self):
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual([], result)

class TestSplitNodesImage(unittest.TestCase):
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
    def test_split_images_no_images_returns_original(self):
        node = TextNode("This has no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This has no images", TextType.TEXT)], new_nodes)
    def test_split_images_preserves_non_text_nodes(self):
        nodes = [
            TextNode("Already link", TextType.LINK, "https://example.com"),
            TextNode("and ![img](https://img.com/a.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Already link", TextType.LINK, "https://example.com"),
                TextNode("and ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://img.com/a.png"),
            ],
            new_nodes,
        )
    def test_split_images_image_at_start(self):
        node = TextNode("![logo](https://img.com/logo.png) trailing text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://img.com/logo.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_images_image_at_end(self):
        node = TextNode("leading text ![logo](https://img.com/logo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("leading text ", TextType.TEXT),
                TextNode("logo", TextType.IMAGE, "https://img.com/logo.png"),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_no_links_returns_original(self):
        node = TextNode("This has no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This has no links", TextType.TEXT)], new_nodes)

    def test_split_links_preserves_non_text_nodes(self):
        nodes = [
            TextNode("already code", TextType.CODE),
            TextNode("click [here](https://example.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("already code", TextType.CODE),
                TextNode("click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_link_at_start(self):
        node = TextNode("[home](https://example.com) page", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("home", TextType.LINK, "https://example.com"),
                TextNode(" page", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        node = TextNode("go to [home](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("go to ", TextType.TEXT),
                TextNode("home", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_ignores_non_h1(self):
        md = "## Subtitle\n# Title\nParagraph"
        self.assertEqual(extract_title(md), "Title")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_extract_title_raises_without_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## No h1 here\nParagraph")

if __name__ == "__main__":
    unittest.main()