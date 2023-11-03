"""Handle CSV files."""

import csv
import logging
import re
from tap_sharepointsites.utils import snakecase

LOGGER = logging.getLogger(__name__)


class CSVHandler:
    """Handle CSV files."""

    def __init__(self, textcontent, delimiter=",", clean_colnames=False):
        """Initialize ExcelHandler."""
        self.textcontent = textcontent
        self.delimiter = delimiter
        self.clean_colnames = clean_colnames

    def get_dictreader(self):
        """Read CSV file and return csv DictReader object for the file."""
        dr = csv.DictReader(
            self.textcontent.splitlines(),
            fieldnames=None,
            restkey="_sdc_extra",
            delimiter=self.delimiter,
        )

        if self.clean_colnames:
            dr.fieldnames = [snakecase(key) for key in dr.fieldnames.copy()]

        return dr
