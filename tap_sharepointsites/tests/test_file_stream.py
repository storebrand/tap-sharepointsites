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
    "files": [{
            "name": "file1",
            "file_pattern": "sample_.*\\.xlsx",
            "file_type": "excel",
            "folder": "sample_folder",
            "clean_colnames": True,
            "delimiter": ";"
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


@pytest.mark.parametrize(
    "filetype, filename, clean_columns, expected_columns",
    [
        ("csv", "sample.csv", True, ["id_column", "first_name", "last_name", "best_invisible_color"]),
        ("csv", "sample.csv", False, ["ID Column", "First Name", "Last Name", "Best (invisible) color"]),
        ("excel", "sample_excel.xlsx", True, ["id_column", "first_name", "last_name", "best_invisible_color"]),
        ("excel", "sample_excel.xlsx", False, ["ID Column", "First Name", "Last Name", "Best (invisible) color"]),
    ],
)
@responses.activate
def test_sync_excel_file_2(mock_az_default_identity, capsys, filetype, filename, clean_columns, expected_columns):

    custom_config = SAMPLE_CONFIG.copy()
    custom_config["files"][0]["clean_colnames"] = clean_columns
    custom_config["files"][0]["file_type"] = filetype
    custom_config["files"][0]["file_pattern"] = filename


    if filetype == "csv":
        content_type = 'text/csv'
    else:
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        

    responses.add_callback(
        responses.GET, 
        re.compile(r'https://m365x214355\.sharepoint\.com/sites/SingerTests/_layouts/15/download\.aspx\?UniqueId=[^&]+'),
        callback=request_callback,
        content_type=content_type,
    )


    responses.add(
        responses.GET,
        f"{custom_config['api_url']}drive",
        json=drive_id_response()
    )

    responses.add(
        GET,
        "https://graph.microsoft.com/v1.0/drives/b!ABCDEFGH1234567890/root:/sample_folder:/children",
        json=list_files_response()
    )

    tap1 = Tapsharepointsites(config=custom_config)
    _ = tap1.streams['file1'].sync(None)

    captured = capsys.readouterr()
    all_stdout = captured.out.strip()
    stdout_parts = [json.loads(row) for row in all_stdout.split('\n')]

    records = [row for row in stdout_parts if row.get('type') == 'RECORD']
    schema = [row for row in stdout_parts if row.get('type') == 'SCHEMA']

    # Test Schema
    assert len(schema) == 1
    keys = list(schema[0]["schema"]["properties"].keys())
    assert keys == expected_columns + ["_sdc_source_file", "_sdc_row_num", "_sdc_loaded_at", "lastModifiedDateTime"]

    # Test Records
    if clean_columns:
        first_names = [row["record"]["first_name"] for row in records]
        last_names = [row["record"]["last_name"] for row in records if row["record"]["last_name"] != '']
    else:
        first_names = [row["record"]["First Name"] for row in records]
        last_names = [row["record"]["Last Name"] for row in records if row["record"]["Last Name"] != '' and row["record"]["Last Name"] is not None]

    assert 'Pippi' in first_names
    assert 'Albert' in first_names


    assert 'Langstrømpe' in last_names
    assert 'Åberg' in last_names

    assert len(last_names) == 2
    assert len(records) == 5


def test_basic_read():
    with open('tap_sharepointsites/tests/configuration/sample.csv', 'r') as file:
        data = file.read()

    assert "Langstrømpe" in data