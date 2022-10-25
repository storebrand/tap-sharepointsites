# flake8: noqa

graph_response_list = """
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#sites('root')/lists('d7689e2b-941a-4cd3-bb24-55cddee54294')/items",
    "@odata.nextLink": "https://graph.microsoft.com/v1.0/sites/root/lists/d7689e2b-941a-4cd3-bb24-55cddee54294/items?$top=1&$skiptoken=UGFnZWQ9VFJVRSZwX0lEPTY",
    "value": [
        {
            "@odata.etag": "c8cf0cd9-826e-4295-8c52-e2c201739dc5,13",
            "createdDateTime": "2017-09-02T01:44:00Z",
            "eTag": "c8cf0cd9-826e-4295-8c52-e2c201739dc5,13",
            "id": "6",
            "lastModifiedDateTime": "2017-09-02T01:45:12Z",
            "webUrl": "https://m365x214355.sharepoint.com/Lists/Office%20365%20Demos/6_.000",
            "createdBy": {
                "user": {
                    "email": "provisioninguser1@m365x214355.onmicrosoft.com",
                    "displayName": "Provisioning User"
                }
            },
            "lastModifiedBy": {
                "user": {
                    "email": "provisioninguser1@m365x214355.onmicrosoft.com",
                    "displayName": "Provisioning User"
                }
            },
            "parentReference": {
                "id": "f392da1c-c8e2-431b-a1a7-ca7f41ade7f3",
                "siteId": "m365x214355.sharepoint.com,5a58bb09-1fba-41c1-8125-69da264370a0,9f2ec1da-0be4-4a74-9254-973f0add78fd"
            },
            "contentType": {
                "id": "0x002B9E68D71A94D34CBB2455CDDEE54294",
                "name": "Office 365 Demos"
            }
        }
    ]
}
"""

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
