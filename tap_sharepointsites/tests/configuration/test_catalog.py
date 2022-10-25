# flake8: noqa

"""Sample catalog for tests."""

sample_catalog = """
{
    "streams": [
      {
        "tap_stream_id": "faker",
        "replication_method": "FULL_TABLE",
        "key_properties": [
          "id"
        ],
        "schema": {
          "properties": {
            "@odata.etag": {
              "type": [
                "string",
                "null"
              ]
            },
            "createdDateTime": {
              "type": [
                "string",
                "null"
              ]
            },
            "eTag": {
              "type": [
                "string",
                "null"
              ]
            },
            "id": {
              "type": [
                "string",
                "null"
              ]
            },
            "lastModifiedDateTime": {
              "type": [
                "string",
                "null"
              ]
            },
            "webUrl": {
              "type": [
                "string",
                "null"
              ]
            },
            "createdBy": {
              "properties": {},
              "type": [
                "object",
                "null"
              ]
            },
            "lastModifiedBy": {
              "properties": {},
              "type": [
                "object",
                "null"
              ]
            },
            "parentReference": {
              "properties": {},
              "type": [
                "object",
                "null"
              ]
            },
            "contentType": {
              "properties": {},
              "type": [
                "object",
                "null"
              ]
            },
            "fields@odata.context": {
              "type": [
                "string",
                "null"
              ]
            },
            "fields": {
              "properties": {},
              "type": [
                "object",
                "null"
              ]
            },
            "_loaded_at": {
              "format": "date-time",
              "type": [
                "string",
                "null"
              ]
            }
          },
          "type": "object"
        },
        "stream": "faker",
        "metadata": [
          {
            "breadcrumb": [
              "properties",
              "@odata.etag"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "createdDateTime"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "eTag"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "id"
            ],
            "metadata": {
              "inclusion": "automatic"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "lastModifiedDateTime"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "webUrl"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "createdBy"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "lastModifiedBy"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "parentReference"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "contentType"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "fields@odata.context"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "fields"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [
              "properties",
              "_loaded_at"
            ],
            "metadata": {
              "inclusion": "available"
            }
          },
          {
            "breadcrumb": [],
            "metadata": {
              "inclusion": "available",
              "selected": true,
              "table-key-properties": [
                "id"
              ]
            }
          }
        ]
      }
    ]
  }
"""
