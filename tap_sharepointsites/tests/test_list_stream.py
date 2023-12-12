import json
from unittest import mock
import pytest
from tap_sharepointsites.list_stream import ListStream
from tap_sharepointsites.tap import Tapsharepointsites
from .configuration.test_catalog import sample_catalog
from .configuration.test_responses import graph_response_list
import logging
import responses
from responses import POST, GET
import re

LOGGER = logging.getLogger("Some logger")

SAMPLE_CONFIG = {
    "api_url": "https://graph.microsoft.com/v1.0/sites/example.sharepoint.com:/sites/demo:/",  # noqa
    "lists": ["list1", "list2"],
}

SAMPLE_CATALOG = json.loads(sample_catalog)
SAMPLE_RESPONSE = json.loads(graph_response_list)


@pytest.fixture
def mock_az_default_identity():
    with mock.patch(
        "azure.identity.DefaultAzureCredential.get_token",
    ) as mock_get_token:
        mock_get_token.return_value = mock.Mock(token="xy-123")
        yield mock_get_token


def test_token(mock_az_default_identity, caplog):
    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG)
    stream1 = ListStream(
        tap=tap1,
        name="teststream",
        path="lists/teststream/items?expand=fields",
    )
    caplog.set_level(logging.INFO)
    LOGGER.info(stream1.authenticator.auth_headers)
    assert stream1.authenticator.auth_headers == {'Authorization': 'Bearer xy-123'}



@responses.activate
def test_stuff(mock_az_default_identity, capsys):

    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG)

    responses.add_callback(
        GET,
        re.compile(r'https://graph.microsoft.com/v1.0/sites/example.sharepoint.com:/sites/demo:/lists/list1/items'),
        callback=lambda _: (200, {}, graph_response_list))

    _ = tap1.streams['list1'].sync(None)


    captured = capsys.readouterr()
    all_stdout = captured.out.strip()
    stdout_parts = all_stdout.split('\n')

    for part in stdout_parts:
        part_json = json.loads(part)
        if part_json['type'] == 'SCHEMA':
            assert part_json['stream'] == 'list1'
            assert part_json['schema']['properties']['id']['type'] == ['string', 'null']
            assert part_json['schema']['properties']['createdDateTime']['type'] == ['string', 'null']
            assert part_json['schema']['properties']['eTag']['type'] == ['string', 'null']
            assert part_json['schema']['properties']['id']['type'] == ['string', 'null']
            assert part_json['schema']['properties']['lastModifiedDateTime']['type'] == ['string', 'null']
            assert part_json['schema']['properties']['webUrl']['type'] == ['string', 'null']
            assert part_json['schema']['properties']['createdBy']['type'] == ['object', 'null']
            assert part_json['schema']['properties']['lastModifiedBy']['type'] == ['object', 'null']
            assert part_json['schema']['properties']['parentReference']['type'] == ['object', 'null']
            assert part_json['schema']['properties']['contentType']['type'] == ['object', 'null']
        if part_json["type"] == 'RECORD':
            assert part_json['stream'] == 'list1'
            assert part_json['record']['id'] == '6'
            assert part_json['record']['createdDateTime'] == '2017-09-02T01:44:00Z'
            assert part_json['record']['eTag'] == 'c8cf0cd9-826e-4295-8c52-e2c201739dc5,13'
            assert part_json['record']['lastModifiedDateTime'] == '2017-09-02T01:45:12Z'
            assert part_json['record']['webUrl'] == 'https://m365x214355.sharepoint.com/Lists/Office%20365%20Demos/6_.000'
            assert part_json['record']['createdBy']['user']['email'] == 'provisioninguser1@m365x214355.onmicrosoft.com'
    assert len(stdout_parts) == 3
    assert 'SCHEMA' in all_stdout
    assert 'RECORD' in all_stdout
    assert 'STATE' in all_stdout


