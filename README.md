# DatabaseRemote (DBRM)

A Python utility library providing high-level interfaces for SQL database operations and data management.

## Overview

DatabaseRemote (DBRM) simplifies database operations by providing intuitive APIs that abstract away complex SQL interactions. The library offers streamlined solutions for common database tasks including data transfer, query generation, and connection management.

## Features

- High-level SQL database interface
- Simplified data transfer between various formats and SQL databases
- Automatic SQL generation and schema handling
- Configurable database operations with sensible defaults
- Connection pooling and management
- Support for batch operations and transaction handling

## Installation

To install DatabaseRemote, clone the repository and install the package using pip:

```bash
git clone https://github.com/wtalioy/DatabaseRemote.git
cd DatabaseRemote
pip install -e .
```

## Usage

### Data Transfer Capabilities

One of the current implementations allows transferring CSV data to SQL tables:

```python
from dbrm import transfer_csv

# Example of transferring data
transfer_csv(
    csv_file="data/sample_data.csv",
    table_name="my_table",
    if_exists="replace",  # Options: "append", "replace", "fail"
)
```

### Working with Large Datasets

```python
from dbrm import transfer_csv

# Process large datasets in manageable chunks
transfer_csv(
    csv_file="data/sample_data2.csv",
    table_name="large_table",
    if_exists="append",
    chunk_size=1000  # Process 1000 rows at a time
)
```

## Configuration

The package should be configured using environment variables. Create a `.env` file in your project root:

```
DB_HOST=localhost
DB_USER=username
DB_PASSWORD=password
DB_NAME=database_name
```

You can also set these variables directly in your environment:

```bash
export DB_HOST=localhost
export DB_USER=username
export DB_PASSWORD=password
export DB_NAME=database_name
```

## Project Structure

```
dbrm/
  ├── __init__.py        # Package exports
  ├── _template.py       # Template utilities
  ├── dbconnector.py     # Database connection management
  ├── remote.py          # Data transfer functionality
  ├── sqlinterpreter.py  # SQL query generation
  ├── sqltable.py        # SQL table operations
  └── utils.py           # Helper utilities
```
