"""sharepointsites tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_sharepointsites.streams import ListStream


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
            required=True,
            description="The name of the list to sync",
        ),
        th.Property(
            "client_id",
            th.DateTimeType,
            required=False,
            description="Managed Identity Client ID",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [
            ListStream(
                tap=self,
                name=list_name,
                path=f"lists/{ list_name }/items?expand=fields",
            )
            for list_name in self.config["lists"]
        ]


if __name__ == "__main__":
    Tapsharepointsites.cli()
