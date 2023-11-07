"""Stream type classes for tap-sharepointsites."""

import datetime
import re
import typing as t
from functools import cached_property
import tempfile
import requests
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from singer_sdk import metrics
from singer_sdk import typing as th
from tap_sharepointsites.client import sharepointsitesStream
from tap_sharepointsites.file_handlers.csv_handler import CSVHandler
from tap_sharepointsites.file_handlers.excel_handler import ExcelHandler
from tap_sharepointsites.utils import snakecase
import textract


class TextStream(sharepointsitesStream):
    """Define custom stream."""

    records_jsonpath = "$.value[*]"
    replication_key = "lastModifiedDateTime"
    primary_keys = ["_sdc_source_file", "_sdc_row_num"]

    # schema_filepath = SCHEMAS_DIR / "files.json"

    def __init__(self, *args, **kwargs):
        """Init CSVStram."""
        # cache text_config so we dont need to go iterating the config list again later

        self.text_config = kwargs.pop("text_config")
        self._header = None
        # self.header = self._get_headers()
        super().__init__(*args, **kwargs)

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        url = "https://graph.microsoft.com/v1.0"

        return url

    def _get_headers(self):
        ad_scope = "https://graph.microsoft.com/.default"

        if self.config.get("client_id"):
            creds = ManagedIdentityCredential(client_id=self.config["client_id"])
        else:
            creds = DefaultAzureCredential()

        token = creds.get_token(ad_scope)

        headers = {
            "Authorization": f"Bearer {token.token}",
        }

        return headers

    @property
    def header(self):
        """Run header function."""
        return self._get_headers()
        # if self._header is None:
        #     self._header = self._get_headers()
        # return self._header

    @property
    def path(self) -> str:
        """Return the API endpoint path, configurable via tap settings."""
        drive_id = self.get_drive_id()
        folder = self.text_config.get("folder")

        if not folder:
            base_url = f"/drives/{drive_id}/root/children"
        else:
            base_url = f"/drives/{drive_id}/root:/{folder}:/children"

        return base_url

    def list_all_files(self, headers=None):
        """List all files in the drive."""
        drive_id = self.get_drive_id()
        folder = self.text_config.get("folder")

        if not folder:
            base_url = (
                f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
            )
        else:
            base_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{folder}:/children"

        while base_url:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            for item in data["value"]:
                if "file" in item:
                    yield item

            base_url = data.get("@odata.nextLink")

    def parse_response(self, response: requests.Response, context) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        resp_values = response.json()["value"]
        files_since = (
            self.get_starting_replication_key_value(context) or "1900-01-01T00:00:00Z"
        )

        for record in resp_values:
            if (
                "file" in record.keys()
                and re.match(self.text_config["file_pattern"], record["name"])
                and record["lastModifiedDateTime"] > files_since
            ):

                file = self.get_file_for_row(record, text=False)

                with tempfile.NamedTemporaryFile(suffix=record["name"]) as tmpfile:
                    tmpfile.write(file)
                    tmpfile.seek(0)
                    text = textract.process(tmpfile.name)

                row = {
                        "content": text.decode("utf-8"),
                        "_sdc_source_file": record["name"],
                        "_sdc_loaded_at": str(datetime.datetime.utcnow()),
                        "lastModifiedDateTime": record["lastModifiedDateTime"],
                    }

                yield row


    schema = th.PropertiesList(
        th.Property(
            "content",
            th.StringType,
        ),
        th.Property(
            "_sdc_source_file",
            th.StringType,
            description="Filename",
        ),
        th.Property(
            "_sdc_loaded_at",
            th.StringType,
            description="Loaded at timestamp",
        ),
        th.Property(
            "lastModifiedDateTime",
            th.StringType,
            description="The last time the file was updated",
        )
    ).to_dict()
    

    def get_drive_id(self):
        """Get drives in the sharepoint site."""
        drive = requests.get(f'{self.config["api_url"]}/drive', headers=self.header)

        if not drive.ok:
            raise Exception(f"Error getting drive: {drive.status_code}: {drive.text}")
        return drive.json()["id"]

    def get_file_for_row(self, row_data, text=True):
        """Get the file for a row."""
        file = requests.get(
            row_data["@microsoft.graph.downloadUrl"], headers=self.header
        )
        file.raise_for_status()

        if text:
            return file.text
        else:
            return file.content

    def get_properties(self, fieldnames) -> dict:
        """Get a list of properties for a *SV file, to be used in creating a schema."""
        properties = {}

        if fieldnames is None:
            msg = (
                "Column names could not be read because they don't exist. Try "
                "manually specifying them using 'delimited_override_headers'."
            )
            raise RuntimeError(msg)
        for field in fieldnames:
            properties.update({field: {"type": ["null", "string"]}})

        return properties

    def request_records(self, context) -> t.Iterable[dict]:
        """Request records from REST endpoint(s), returning response records.

        If pagination is detected, pages will be recursed automatically.

        Args:
            context: Stream partition or context dictionary.

        Yields
        ------
            An item for every record in the response.

        """
        paginator = self.get_new_paginator()

        decorated_request = self.request_decorator(self._request)

        with metrics.http_request_counter(self.name, self.path) as request_counter:
            request_counter.context = context

            while not paginator.finished:
                prepared_request = self.prepare_request(
                    context,
                    next_page_token=paginator.current_value,
                )
                resp = decorated_request(prepared_request, context)
                request_counter.increment()
                self.update_sync_costs(prepared_request, resp, context)

                yield from self.parse_response(resp, context)

                paginator.advance(resp)

    def get_records(self, context):
        """Return a generator of record-type dictionary objects.

        Each record emitted should be a dictionary of property names to their values.

        Args:
            context: Stream partition or context dictionary.

        Yields
        ------
            One item per (possibly processed) record in the API.

        """
        for record in self.request_records(context):
            transformed_record = self.post_process(record, context)
            if transformed_record is None:
                # Record filtered out during post_process()
                continue
            yield transformed_record
