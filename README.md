# DatabaseRemote (DBRM)

A Python utility library providing SQLAlchemy-like interfaces for SQL database operations and data management.

## Overview

DatabaseRemote (DBRM) simplifies database operations by providing intuitive, SQLAlchemy-inspired APIs that abstract away complex SQL interactions. The library offers streamlined solutions for common database tasks including data transfer, query generation, and connection management.

## Features

- SQLAlchemy-like interface with fluent query building
- Declarative table definitions
- Session-based transaction management
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

### Engine and Session Management

Creating a database connection using the Engine and Session classes:

```python
from dbrm import Engine, Session

# Create a database engine from environment variables
engine = Engine.from_env()

# Use a session for database operations
with Session(engine) as session:
    # Execute raw SQL
    result = session.execute("SELECT * FROM users")
    for row in result.fetchall():
        print(row)
    
    # With transaction management
    with session.begin():
        session.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                      ("John Doe", "john@example.com"))
        # Transaction automatically committed unless an exception occurs
```

### Declarative Table Definitions

Define tables using SQLAlchemy-like declarative syntax:

```python
from dbrm import Table, Column, Integer, String, Boolean

# Define a table
class User(Table):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    active = Column(Boolean, default=True)

# Create the table in the database
with Session(engine) as session:
    User.create(session)
```

### Building Queries with Fluent Interface

The library provides a fluent interface for building SQL queries:

```python
from dbrm import Select, Insert, Update, Delete

# SELECT queries
query = Select("id", "name").from_("users").where("age > 21").order_by("name")
with Session(engine) as session:
    result = query.execute(session)
    for row in result.fetchall():
        print(row)

# INSERT operations
with Session(engine) as session:
    Insert("users").values(
        name="Jane Smith",
        email="jane@example.com",
        age=28
    ).execute(session)
    session.commit()

# UPDATE operations
with Session(engine) as session:
    Update("users").set(
        active=False
    ).where("last_login < '2023-01-01'").execute(session)
    session.commit()

# DELETE operations
with Session(engine) as session:
    Delete("users").where("active = False").execute(session)
    session.commit()
```

### Data Transfer Capabilities

Transfer CSV data to SQL tables:

```python
from dbrm import Engine, transfer_csv

# Create engine
engine = Engine.from_env()

# Example of transferring data
transfer_csv(
    csv_file="data/sample_data.csv",
    table_name="my_table",
    engine=engine,
    if_exists="replace",  # Options: "append", "replace", "fail"
)
```

## Configuration

The package should be configured using environment variables. Create a `.env` file in your project root:

```
DRIVER=ODBC Driver 17 for SQL Server
SERVER=localhost
DATABASE=mydatabase
UID=username
PWD=password
```

You can also set these variables directly in your environment:

```bash
export DRIVER="ODBC Driver 17 for SQL Server"
export SERVER=localhost
export DATABASE=mydatabase
export UID=username
export PWD=password
```

## Project Structure

```
dbrm/
  ├── __init__.py        # Package exports and types
  ├── engine.py          # SQLAlchemy-like engine for connection management
  ├── session.py         # Session class for transaction management
  ├── schema.py          # Declarative table definitions
  ├── query.py           # Fluent query builders (Select, Insert, Update, Delete)
  ├── remote.py          # Data transfer functionality
  ├── utils.py           # Helper utilities and type mappings
  ├── _template.py       # Template utilities (legacy)
  ├── dbconnector.py     # Database connection management (legacy)
  ├── sqlinterpreter.py  # SQL query generation (legacy)
  └── sqltable.py        # SQL table operations (legacy)
```

## Type System

DBRM provides SQL type mappings for Python types:

```python
from dbrm import Integer, String, Float, Boolean, DateTime, Text, Date, JSON, BLOB

# Use these types when defining columns
class Product(Table):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float)
    created_at = Column(DateTime)
    metadata = Column(JSON)
```

## Advanced Features

### Joins

You can create JOIN queries with the fluent interface:

```python
query = (Select("u.name", "o.product_name", "o.quantity")
         .from_("users u")
         .join("orders o", "u.id = o.user_id")
         .where("o.status = 'shipped'"))

with Session(engine) as session:
    results = query.execute(session).fetchall()
```