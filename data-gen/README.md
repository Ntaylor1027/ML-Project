# Data Generator

This is our data generation tool used for the Blast Radius Project.

## Dependencies

The tool uses the following Python packages (Brief Descriptions commented by
import statements in code).

1. Docopt - creates a command-line interface from docstrings
2. Faker - generates fake PII information

## CLI

See [Command Usage](https://github.com/bennettca/blast-radius/blob/master/data-gen/main.py#L1)

## Setup

- Install Python and Pip.
- [pipenv](https://github.com/pypa/pipenv) creates a virtualized Python environment for specific
  Python versions and package dependencies (defined by [Pipfile](Pipfile)). Install pipenv: `pip install pipenv`
- In this directory, run `pipenv install` to install dependencies.
- To run the data-gen program, `pipenv run ./main.py` to execute `main.py` in the virtualized environment.
- Alternatively, `pipenv shell` to enter the virtualized environment and execute shell commands.

## Command Output

- `%.csv` - comma-separated values of text which can contain PII information
- `%-meta.json` - maps each CSV line to a list of labeled PII entities in a given line
