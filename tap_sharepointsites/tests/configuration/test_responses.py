# flake8: noqa


catalog_json = """
{
  "streams": [
    {
      "tap_stream_id": "lists",
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
            "type": [
              "string",
              "null"
            ]
          },
          "lastModifiedBy": {
            "type": [
              "string",
              "null"
            ]
          },
          "parentReference": {
            "type": [
              "string",
              "null"
            ]
          },
          "contentType": {
            "type": [
              "string",
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
            "type": [
              "string",
              "null"
            ]
          }
        },
        "type": "object"
      },
      "stream": "lists",
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
