"""Stream for Pages - most relevant for LLM stuff."""

import datetime
import typing as t

import requests
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from selectolax.parser import HTMLParser
from singer_sdk import metrics
from singer_sdk.typing import IntegerType, PropertiesList, Property, StringType

from tap_sharepointsites.client import sharepointsitesStream


class PagesStream(sharepointsitesStream):
    """Define custom stream."""

    records_jsonpath = "$.value[*]"
    replication_key = "lastModifiedDateTime"
    primary_keys = ["_sdc_source_file", "_sdc_chunk_number"]

    def __init__(self, *args, **kwargs):
        """Init Page Stream."""
        self._header = None
        # self.header = self._get_headers()
        super().__init__(*args, **kwargs)

    def _get_headers(self):
        """Get adhoc headers for request."""
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

    name = "pages"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://graph.microsoft.com"

    @property
    def header(self):
        """Run header function."""
        return self._get_headers()

    @property
    def path(self) -> str:
        """Return the API endpoint path, configurable via tap settings."""
        base_url = f"/beta/sites/{self.site_id}/pages"

        return base_url

    @staticmethod
    def simple_chunker(text: str, chunk_length: int) -> list:
        """Split a text into N chunks of a fixed size, leaving the remainder in the last chunk."""
        text_array = text.split(" ")
        text_length = len(text_array)
        # chunk_length = text_length // num_chunks
        num_chunks = text_length // chunk_length + 1
        chunks = []

        for i in range(num_chunks):
            start = i * chunk_length
            end = start + chunk_length if i < num_chunks - 1 else text_length
            chunks.append(" ".join(text_array[start:end]))

        return chunks

    @property
    def schema(self):
        """Return a schema object for this stream."""
        schema = PropertiesList(
            Property("title", StringType),
            Property("content", StringType),
            Property("eTag", StringType),
            Property("id", StringType),
            Property("lastModifiedDateTime", StringType),
            Property("_sdc_source_id", StringType),
            Property("_sdc_loaded_at", StringType()),
            Property("_sdc_chunk_num", IntegerType()),
        ).to_dict()
        return schema

    @property
    def site_id(self):
        """Return ID of specified Sharepoint Site."""
        full_url = self.config.get("api_url")
        response = requests.get(full_url, headers=self.header)
        return response.json()["id"]

    def parse_response(self, response: requests.Response, context) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        resp_values = response.json()["value"]
        files_since = (
            self.get_starting_replication_key_value(context) or "1900-01-01T00:00:00Z"
        )

        for record in resp_values:
            if record["lastModifiedDateTime"] > files_since:

                page_element = self.get_content_for_page(record["id"])

                chunks = self.simple_chunker(page_element, 3000)
                for j, chunk in enumerate(chunks):
                    record = {
                        "title": record["title"],
                        "content": chunk,
                        "lastModifiedDateTime": record["lastModifiedDateTime"],
                        "_sdc_source_id": record["id"],
                        "_sdc_loaded_at": str(datetime.datetime.utcnow()),
                        "_sdc_chunk_num": j,
                    }

                    yield record

    def get_content_for_page(self, id):
        """Get content for page."""
        base_url = (
            f"https://graph.microsoft.com/beta/sites/{self.site_id}/pages/"
            f"{id}/microsoft.graph.sitepage/webparts"
        )

        page_content = requests.get(base_url, headers=self.header)
        page_content.raise_for_status()

        data = page_content.json()
        htmls = "".join(
            [
                element.get("innerHtml")
                for element in data["value"]
                if element.get("innerHtml")
            ]
        )

        parsed_htmls = self.parse_html(htmls)

        return parsed_htmls

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

    @staticmethod
    def parse_html(html_string: str):
        """Parse html string and return decently formatted text."""
        unwrap_tags = ["em", "strong", "b", "i", "span", "a", "code", "kbd"]
        remove_tags = ["script", "style"]

        parsed_html = HTMLParser(html_string)
        for removed_tag in remove_tags:
            for element in parsed_html.css(removed_tag):
                element.decompose()

        parsed_html.unwrap_tags(unwrap_tags)
        html_texts = []
        for node in parsed_html.css("*"):
            # selectolax `strip=True` will merge unwrapped tag texts together
            # so we need regular python strip()
            node_text = node.text(deep=False, strip=False)
            node_text = node_text.strip()
            node_text = node_text.replace("\n", " ")
            if node_text:
                html_texts.append(node_text)
        return "\n".join(html_texts)
