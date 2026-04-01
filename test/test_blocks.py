import unittest

from src.blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_level_1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_invalid_no_space(self):
        block = "##Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_invalid_too_many_hashes(self):
        block = "####### Too many"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_single_line(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_multiline(self):
        block = "```\nline1\nline2\nline3\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_invalid_missing_closing(self):
        block = "```\nprint('oops')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_single_line(self):
        block = "> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_multiline(self):
        block = "> quote one\n>quote two\n> quote three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_invalid_mixed_lines(self):
        block = "> quote\nnot quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid_missing_space(self):
        block = "-item one\n-item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_starts_at_two(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_skips_number(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_block(self):
        block = "This is a regular paragraph.\nStill paragraph text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_markdown_to_blocks_only_newlines(self):
        self.assertEqual(markdown_to_blocks("\n\n\n\n"), [])

    def test_markdown_to_blocks_strips_block_whitespace(self):
        md = "   first block   \n\n   second block   "
        self.assertEqual(markdown_to_blocks(md), ["first block", "second block"])

    def test_markdown_to_blocks_many_blank_lines_between_blocks(self):
        md = "first\n\n\n\nsecond\n\n\nthird"
        self.assertEqual(markdown_to_blocks(md), ["first", "second", "third"])

    def test_markdown_to_blocks_single_block(self):
        md = "line one\nline two\nline three"
        self.assertEqual(markdown_to_blocks(md), ["line one\nline two\nline three"])
        
    def test_markdown_to_blocks_preserves_internal_newlines(self):
        md = "para line 1\npara line 2\n\nnext block"
        self.assertEqual(md_to_blocks := markdown_to_blocks(md), ["para line 1\npara line 2", "next block"])


if __name__ == "__main__":
    unittest.main()