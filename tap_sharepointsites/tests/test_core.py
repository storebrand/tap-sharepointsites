"""Tests standard tap features using the built-in SDK tests library."""

import json
from unittest import mock

import pytest

from tap_sharepointsites.list_stream import ListStream
from tap_sharepointsites.tap import Tapsharepointsites

from .configuration.test_catalog import sample_catalog

SAMPLE_CONFIG = {
    "api_url": "https://graph.microsoft.com/v1.0/sites/example.sharepoint.com:/sites/demo:/",  # noqa
    "lists": ["list1", "list2"],
}

SAMPLE_CATALOG = json.loads(sample_catalog)
list_response_paginated = json.loads(
    open("tap_sharepointsites/tests/configuration/list_response_paginated.json").read()
)  # noqa


def test_cli_prints() -> None:
    # Initialize with basic config
    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG)
    # Test CLI prints
    tap1.print_version()
    tap1.print_about()


def test_discovery() -> None:
    catalog1 = json.loads(sample_catalog)

    # Reset and re-initialize with an input catalog
    tap2 = Tapsharepointsites(config=SAMPLE_CONFIG, catalog=catalog1)
    assert tap2


def test_get_url():
    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG)
    stream1 = ListStream(
        tap=tap1,
        name="teststream",
        path="lists/teststream/items?expand=fields",
    )

    assert stream1.get_url({}).startswith(
        "https://graph.microsoft.com/v1.0/sites/example.sharepoint.com:/sites/demo:/"
    )


def test_next_page():
    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG)
    stream1 = ListStream(
        tap=tap1,
        name="teststream",
        path="lists/teststream/items?expand=fields",
    )
    resp = mock.MagicMock()
    resp.json.return_value = list_response_paginated

    paginator = stream1.get_new_paginator()
    next_url = paginator.get_next_url(resp)
    assert (
        next_url
        == "https://graph.microsoft.com/v1.0/sites/root/lists/d7689e2b-941a-4cd3-bb24-55cddee54294/items?$top=1&$skiptoken=UGFnZWQ9VFJVRSZwX0lEPTY"  # noqa
    )


@pytest.fixture
def mock_get_token():
    with mock.patch(
        "tap_sharepointsites.list_stream.ListStream.authenticator",
        new_callable=mock.PropertyMock,
    ) as mock_get_token:
        mock_get_token.return_value = "token"
        yield mock_get_token


def test_token(mock_get_token):
    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG)
    stream1 = ListStream(
        tap=tap1,
        name="teststream",
        path="lists/teststream/items?expand=fields",
    )

    assert stream1.authenticator == "token"
