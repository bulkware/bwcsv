"""Display-free tests for table-search matching."""

import unittest

from bwcsv.functions import find_string


class FindStringTests(unittest.TestCase):
    """Keep search behaviour predictable for table cells."""

    def test_finds_text_with_matching_case(self):
        """A literal query matches a substring by default."""
        self.assertTrue(find_string("bulk", "bulkware"))

    def test_can_ignore_case(self):
        """Case-insensitive search finds differently cased text."""
        self.assertTrue(find_string("BULK", "bulkware", ignorecase=True))
        self.assertFalse(find_string("BULK", "bulkware"))

    def test_whole_word_search_excludes_partial_matches(self):
        """Whole-word mode does not select parts of a larger word."""
        self.assertTrue(find_string("csv", "open csv file", wholeword=True))
        self.assertFalse(find_string("csv", "bwcsv", wholeword=True))

    def test_escapes_regular_expression_characters(self):
        """User input is always interpreted as literal text."""
        self.assertTrue(find_string("[1]", "row [1]"))
        self.assertFalse(find_string("[1]", "row 1"))

    def test_empty_query_or_subject_never_matches(self):
        """Empty values must not make every table cell a result."""
        self.assertFalse(find_string("", "value"))
        self.assertFalse(find_string("value", ""))
