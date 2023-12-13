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
import csv

LOGGER = logging.getLogger("Some logger")


SAMPLE_CONFIG = {
    "api_url": "https://graph.microsoft.com/v1.0/sites/m365x214355.sharepoint.com:/sites/SingerTests:/",  # noqa
    "text_files": [
        {
            "name": "file1",
            "file_pattern": "sample.*",
            "folder": "sample_folder",
        }
    ]
}


def request_callback(request):
    if request.url.endswith("excel"):
        with open('tap_sharepointsites/tests/configuration/sample_excel.xlsx', 'rb') as file:
            excel_data = file.read()

        return (200, {'Content-Disposition': 'attachment; filename="demo.xlsx"'}, excel_data)
    else:
        with open('tap_sharepointsites/tests/configuration/sample.csv', 'r', encoding='utf-8') as file:
            csv_data = file.read()

        return (200, {'Content-Disposition': 'attachment; filename="sample.csv"', 
                      'Content-Type': 'text/csv; charset=utf-8'}, csv_data)


def drive_id_response():
    js = json.loads(open('tap_sharepointsites/tests/configuration/drive_id_response.json', 'r').read())
    return js


def list_files_response():
    js = json.loads(open('tap_sharepointsites/tests/configuration/file_info_response.json', 'r').read())
    return js


@pytest.fixture
def mock_az_default_identity():
    with mock.patch(
        "azure.identity.DefaultAzureCredential.get_token",
    ) as mock_get_token:
        mock_get_token.return_value = mock.Mock(token="xy-123")
        yield mock_get_token


@responses.activate
def test_text(mock_az_default_identity, capsys):

    responses.add_callback(
        responses.GET, 
        re.compile(r'https://m365x214355\.sharepoint\.com/sites/SingerTests/_layouts/15/download\.aspx\?UniqueId=[^&]+'),
        callback=request_callback
    )


    responses.add(
        responses.GET,
        f"{SAMPLE_CONFIG['api_url']}drive",
        json=drive_id_response()
    )

    responses.add(
        GET,
        "https://graph.microsoft.com/v1.0/drives/b!ABCDEFGH1234567890/root:/sample_folder:/children",
        json=list_files_response()
    )

    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG)
    _ = tap1.streams['file1'].sync(None)

    captured = capsys.readouterr()
    all_stdout = captured.out.strip()
    stdout_parts = [json.loads(row) for row in all_stdout.split('\n')]

    records = [row for row in stdout_parts if row.get('type') == 'RECORD']
    schema = [row for row in stdout_parts if row.get('type') == 'SCHEMA']

    # Test Schema
    assert len(schema) == 1
    assert len(records) == 2
    assert 'Langstrømpe' in records[0]['record']['content']