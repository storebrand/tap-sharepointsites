"""Utility functions for tap-sharepointsites."""

import re


def snakecase(name):
    """Convert a string to snake_case."""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)

    # Replace any non-alphanumeric characters with underscores
    name = re.sub(r"[^a-zA-Z0-9_]+", "_", name)

    # Replace any sequence of multiple underscores with a single underscore
    name = re.sub(r"_{2,}", "_", name)

    return name.lower()
