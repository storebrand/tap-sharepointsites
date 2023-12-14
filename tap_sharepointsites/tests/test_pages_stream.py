import json
import logging
from unittest import mock

import pytest
import responses
from responses import GET

from tap_sharepointsites.tap import Tapsharepointsites

LOGGER = logging.getLogger("Some logger")


SAMPLE_CONFIG = {
    "api_url": "https://graph.microsoft.com/v1.0/sites/m365x214355.sharepoint.com:/sites/SingerTests:/",  # noqa
    "pages": True,
}


@pytest.fixture
def mock_az_default_identity():
    with mock.patch(
        "azure.identity.DefaultAzureCredential.get_token",
    ) as mock_get_token:
        mock_get_token.return_value = mock.Mock(token="xy-123")
        yield mock_get_token


def mock_pages_response():
    with open(
        "tap_sharepointsites/tests/configuration/pages_response.json", "r"
    ) as file:
        js = json.load(file)
    return js


def mock_page1_response():
    with open(
        "tap_sharepointsites/tests/configuration/page_1_response.json", "r"
    ) as file:
        js = json.load(file)
    return js


def mock_page2_response():
    with open(
        "tap_sharepointsites/tests/configuration/page_2_response.json", "r"
    ) as file:
        js = json.load(file)
    return js


def mock_site_response():
    with open(
        "tap_sharepointsites/tests/configuration/site_response.json", "r"
    ) as file:
        js = json.load(file)
    return js


@responses.activate
def test_pages(mock_az_default_identity, capsys):

    responses.add(
        GET,
        "https://graph.microsoft.com/beta/sites/m365x214355.sharepoint.com,5a58bb09-1fba-41c1-8125-69da264370a0,9f2ec1da-0be4-4a74-9254-973f0add78fd/pages",  # noqa
        json=mock_pages_response(),
        status=200,
    )

    responses.add(
        GET,
        "https://graph.microsoft.com/beta/sites/m365x214355.sharepoint.com,5a58bb09-1fba-41c1-8125-69da264370a0,9f2ec1da-0be4-4a74-9254-973f0add78fd/pages/111-bfsv-bfdv-bfdsb-bvfedabgtf/microsoft.graph.sitepage/webparts",  # noqa
        json=mock_page1_response(),
        status=200,
    )

    responses.add(
        GET,
        "https://graph.microsoft.com/beta/sites/m365x214355.sharepoint.com,5a58bb09-1fba-41c1-8125-69da264370a0,9f2ec1da-0be4-4a74-9254-973f0add78fd/pages/222-bfsv-bfdv-bfdsb-bvfedabgtf/microsoft.graph.sitepage/webparts",  # noqa
        json=mock_page2_response(),
        status=200,
    )

    responses.add(
        GET,
        SAMPLE_CONFIG["api_url"],
        json=mock_site_response(),
        status=200,
    )

    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG)
    _ = tap1.streams["pages"].sync(None)

    captured = capsys.readouterr()
    all_stdout = captured.out.strip()

    stdout_parts = [json.loads(row) for row in all_stdout.split("\n")]

    records = [row for row in stdout_parts if row.get("type") == "RECORD"]
    schema = [row for row in stdout_parts if row.get("type") == "SCHEMA"]

    # Test Schema
    assert len(schema) == 1
    assert len(records) == 2
    assert "Furry Communities" in all_stdout
    assert "<p>" not in all_stdout
    assert "Early Cryptocurrency Scams" in all_stdout
