# ⚠️ This repository is no longer being maintained
Storebrand have moved on from Meltano, and we're therefore no longer maintaining this repository. 

# tap-sharepointsites

`tap-sharepointsites` is a Singer tap for Microsoft Graph Sharepoint lists.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

[![Test tap-sharepointsites](https://github.com/radbrt/tap-sharepointsites/actions/workflows/ci_workflow.yml/badge.svg)](https://github.com/radbrt/tap-sharepointsites/actions/workflows/ci_workflow.yml)

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`

## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| api_url             | True     | None    | The url for the API service |
| lists               | False    | None    | The name of the list to sync |
| files               | False    | None    | Files to sync |
| pages               | False    | None    | Whether or not to sync pages |
| client_id           | False    | None    | Managed Identity Client ID |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |
| batch_config        | False    | None    |             |

A full list of supported settings and capabilities is available by running: `tap-sharepointsites --about`


## File config

The file configuration accepts an array of objects, with keys: 
- `name`: Name given to the stream/table 
- `file_pattern`: regex-like pattern for filenames to load
- `folder`: Subfolder where the files are located
- `file_type`: Type (format) of file to load, either `csv` or `excel`.
- `delimiter`: Field delimiter for CSV files. default `,`
- `clean_colnames`: Whether to convert column names to snake_case. default `false`

Example config:

```
...
  config:
    ...
    files:
    - name: employees
      file_pattern: employees_.*\.csv
      folder: hr_data/raw
      file_type: csv
      clean_colnames: true
  ...
```

## Web pages

You can sync the content of sharepoint web pages, typically relevant for LLM/RAG type of use cases. The Microsoft Graph endpoint for pages is still in Beta, and does not work when logged in as a personal user. In order for it to work, you need to use a Managed Identity.

Example config:

```
...
  config:
    ...
    pages: true
  ...
```


<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

## Installation

Install from PyPi:

```bash
pipx install tap-sharepointsites
```

Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-sharepointsites.git@main
```

-->

## Configuration

### Accepted Config Options

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```
tap-sharepointsites --about --format=markdown
```
-->

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-sharepointsites --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization


<!--
Developer TODO: If your tap requires special access on the source system, or any special authentication requirements, provide those here.
-->

## Usage

You can easily run `tap-sharepointsites` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-sharepointsites --version
tap-sharepointsites --help
tap-sharepointsites --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_sharepointsites/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-sharepointsites` CLI interface directly using `poetry run`:

```bash
poetry run tap-sharepointsites --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-sharepointsites
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-sharepointsites --version
# OR run a test `elt` pipeline:
meltano elt tap-sharepointsites target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
