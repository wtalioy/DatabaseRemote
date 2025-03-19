from dbrm.template import *

dtype_mapping = {
    'int64': 'INTEGER',
    'int32': 'INTEGER',
    'float64': 'FLOAT',
    'float32': 'FLOAT',
    'bool': 'BOOLEAN',
    'datetime64[ns]': 'DATETIME',
    'object': 'VARCHAR(255)',
    'category': 'VARCHAR(255)',
    'text': 'TEXT',
}


def create_table(table_name: str, column_info: tuple) -> str:
    """
    Generate SQL code to create a table with the specified name and columns.

    Args:
        table_name (str): The name of the table to create.
        column_info (tuple): A tuple of tuples, where each tuple contains the column name, its data type and length.

    Returns:
        str: The SQL code to create the table.
    """
    column_definitions = []
    for col_name, dtype, length in column_info:
        if dtype not in dtype_mapping:
            raise ValueError(f"Unsupported data type: {dtype}")
        if dtype != 'object':
            column_definitions.append(f"{col_name} {dtype_mapping[dtype]}")
        elif length is not None:
            column_definitions.append(f"{col_name} {dtype_mapping['object']}({length})")
        else:
            column_definitions.append(f"{col_name} {dtype_mapping['object']}(50)")
    column_definitions = ', '.join(column_definitions)
    sql_str = CREATE_TABLE.format(table_name, column_definitions)
    return sql_str


def drop_table(table_name: str) -> str:
    """
    Generate SQL code to drop a table with the specified name.

    Args:
        table_name (str): The name of the table to drop.

    Returns:
        str: The SQL code to drop the table.
    """
    sql_str = DROP_TABLE.format(table_name)
    return sql_str


def select(column_names: str | tuple, table_names: str | tuple, conditions: str | tuple) -> str:
    """
    Generate SQL code to select data from a table.

    Args:
        column_names (str | tuple): The columns to select.
        table_names (str | tuple): The tables to select from.
        conditions (str | tuple): The conditions for the selection.

    Returns:
        str: The SQL code to select data from the table.
    """
    columns = ', '.join(column_names) if isinstance(column_names, tuple) else column_names
    tables = ', '.join(table_names) if isinstance(table_names, tuple) else table_names
    conditions_str = ' AND '.join(conditions) if isinstance(conditions, tuple) else conditions
    sql_str = SELECT.format(columns, tables, conditions_str)
    return sql_str


def insert_into_table(table_name: str, column_names: str | tuple, values) -> str:
    """
    Generate SQL code to insert data into a table.

    Args:
        table_name (str): The name of the table to insert data into.
        column_names (str | tuple): A tuple of column names to insert data into.
        values (any): values to insert.

    Returns:
        str: The SQL code to insert data into the table.
    """
    columns = ', '.join(column_names) if isinstance(column_names, tuple) else column_names
    sql_str = INSERT.format(table_name, columns, values)
    return sql_str


