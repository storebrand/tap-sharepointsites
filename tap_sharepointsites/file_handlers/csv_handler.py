"""Handle CSV files."""

import csv
import logging
import re

LOGGER = logging.getLogger(__name__)


class CSVHandler:
    """Handle CSV files."""

    def __init__(self, textcontent, delimiter=","):
        """Initialize ExcelHandler."""
        self.textcontent = textcontent
        self.delimiter = delimiter

    @staticmethod
    def format_key(key):
        """Format key."""
        formatted_key = re.sub(r"[^\w\s]", "", key)
        formatted_key = re.sub(r"\s+", "_", formatted_key)
        return formatted_key.lower()

    def get_dictreader(self):
        """Read CSV file and return csv DictReader object for the file."""
        dr = csv.DictReader(
            self.textcontent.splitlines(),
            fieldnames=None,
            restkey="_sdc_extra",
            delimiter=self.delimiter,
        )

        dr.fieldnames = [self.format_key(key) for key in dr.fieldnames.copy()]

        return dr
