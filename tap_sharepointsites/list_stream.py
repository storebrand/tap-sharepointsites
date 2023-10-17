"""Stream type classes for tap-sharepointsites."""

from pathlib import Path

from singer_sdk.helpers._typing import TypeConformanceLevel
from singer_sdk.typing import (
    DateTimeType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)

from tap_sharepointsites.client import sharepointsitesStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ListStream(sharepointsitesStream):
    """Define custom stream."""

    records_jsonpath = "$.value[*]"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    primary_keys = ["id"]
    replication_key = None

    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY

    schema = PropertiesList(
        Property("@odata.etag", StringType),
        Property("createdDateTime", StringType),
        Property("eTag", StringType),
        Property("id", StringType),
        Property("lastModifiedDateTime", StringType),
        Property("webUrl", StringType),
        Property("createdBy", ObjectType()),
        Property("lastModifiedBy", ObjectType()),
        Property("parentReference", ObjectType()),
        Property("contentType", ObjectType()),
        Property("fields@odata.context", StringType),
        Property("fields", ObjectType()),
        Property("_loaded_at", DateTimeType),
    ).to_dict()
