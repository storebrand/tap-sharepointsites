"""sharepointsites tap class."""

import json
import os
from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_sharepointsites.file_stream import FilesStream
from tap_sharepointsites.list_stream import ListStream


class Tapsharepointsites(Tap):
    """sharepointsites tap class."""

    name = "tap-sharepointsites"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_url",
            th.StringType,
            required=True,
            description="The url for the API service",
        ),
        th.Property(
            "lists",
            th.ArrayType(th.StringType),
            required=False,
            description="The name of the list to sync",
        ),
        th.Property(
            "files",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "name",
                        th.StringType,
                        required=True,
                        description="The name of the stream",
                    ),
                    th.Property(
                        "file_pattern",
                        th.StringType,
                        required=True,
                        description="The file pattern to match",
                    ),
                    th.Property(
                        "file_type",
                        th.StringType,
                        required=True,
                        description="The file type to match",
                    ),
                    th.Property(
                        "delimiter",
                        th.StringType,
                        required=False,
                        description="For CSV files: the delimiter to use",
                    ),
                    th.Property(
                        "clean_colnames",
                        th.BooleanType,
                        required=False,
                        default=False,
                        description="Replace special characters and convert to snakecase",
                    ),
                ),
            ),
            required=False,
            description="Files to sync",
        ),
        th.Property(
            "client_id",
            th.DateTimeType,
            required=False,
            description="Managed Identity Client ID",
        ),
    ).to_dict()

    def get_file_configs(self) -> List[dict]:
        """Return a list of file configs.

        Either directly from the config.json or in an external file
        defined by csv_files_definition.
        """
        csv_files = self.config.get("files")
        csv_files_definition = self.config.get("csv_files_definition")
        if csv_files_definition:
            if os.path.isfile(csv_files_definition):
                with open(csv_files_definition, "r") as f:
                    csv_files = json.load(f)
            else:
                self.logger.error(
                    f"tap-sharepoint: '{csv_files_definition}' file not found"
                )
                exit(1)
        if not csv_files:
            self.logger.error("No CSV file definitions found.")
            exit(1)
        return csv_files

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        if self.config.get("lists"):
            list_streams = [
                ListStream(
                    tap=self,
                    name=list_name,
                    path=f"lists/{ list_name }/items?expand=fields",
                )
                for list_name in self.config["lists"]
            ]
        else:
            list_streams = []

        if self.config.get("files"):
            files_streams = [
                FilesStream(
                    tap=self,
                    name=file["name"],
                    file_config=file,
                )
                for file in self.config["files"]
            ]
        else:
            files_streams = []

        all_streams = list_streams + files_streams

        self.logger.info(f"Discovered {len(all_streams)} streams")

        return all_streams


if __name__ == "__main__":
    Tapsharepointsites.cli()
