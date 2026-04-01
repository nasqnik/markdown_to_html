import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
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
        
    def test_to_html_raises_when_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_raises_when_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " normal "),
                LeafNode("i", "italic"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold</b> normal <i>italic</i></p>")

    def test_to_html_with_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_parent_props(self):
        node = ParentNode("a", [LeafNode(None, "Click me")], {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me</a>')

    def test_to_html_deeply_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode("p", [LeafNode("span", "nested")]),
                    ],
                )
            ],
        )
        self.assertEqual(node.to_html(), "<div><section><p><span>nested</span></p></section></div>")

if __name__ == "__main__":
    unittest.main()