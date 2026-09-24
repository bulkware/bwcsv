"""Display-free tests for CSV parsing."""

from pathlib import Path
import tempfile
import unittest

from bwcsv.csvparser import CSVParser


class CSVParserTests(unittest.TestCase):
    """Verify the parser's success and error states."""

    def test_loads_utf8_csv_with_consistent_columns(self):
        """A valid CSV file exposes its rows and dimensions."""
        # Spreadsheet exports often include a BOM, which must not become data.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "people.csv"
            path.write_text("name,city\nAda,Helsinki\n", encoding="utf-8")

            parser = CSVParser()

            self.assertTrue(parser.load_file(str(path)))
            self.assertEqual(parser.columncount, 2)
            self.assertEqual(parser.rowcount, 2)
            self.assertEqual(parser.filedata[1], ["Ada", "Helsinki"])

    def test_rejects_empty_csv(self):
        """An empty file has no table shape and is not opened."""
        # Empty input cannot define a table shape for the viewer.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_text("", encoding="utf-8")

            parser = CSVParser()

            self.assertFalse(parser.load_file(str(path)))
            self.assertEqual(parser.message, "Error: CSV file is empty.")

    def test_rejects_inconsistent_rows(self):
        """A malformed table cannot later fail while populating the GUI."""
        # The table widget relies on every parsed row having the same width.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.csv"
            path.write_text("one,two\nthree\n", encoding="utf-8")

            parser = CSVParser()

            self.assertFalse(parser.load_file(str(path)))
            self.assertIn("consistent", parser.message)
