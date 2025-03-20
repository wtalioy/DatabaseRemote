from .template import *
from .utils import DTYPE_MAPPING, check_size, process_value


def create_table(table_name: str, column_info: tuple | list) -> str:
    """
    Generate SQL code to create a table with the specified name and columns.

    Args:
        table_name (str): The name of the table to create.
        column_info (tuple | list): A tuple or list of tuples/lists, where each contains the column name, its data type and length.

    Returns:
        str: The SQL code to create the table.
    """
    column_definitions = []
    for col_name, dtype, length in column_info:
        if dtype not in DTYPE_MAPPING:
            raise ValueError(f"Unsupported data type: {dtype}")
        if dtype == 'object':
            if length is not None:
                column_definitions.append(f"{col_name} {DTYPE_MAPPING[dtype]}({length})")
            else:
                column_definitions.append(f"{col_name} {DTYPE_MAPPING[dtype]}(255)")
        else:
            column_definitions.append(f"{col_name} {DTYPE_MAPPING[dtype]}")
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


def where(condition: str | tuple | list) -> str:
    """
    Generate SQL code for a WHERE clause.

    Args:
        condition (str | tuple | list): The condition for the WHERE clause.

    Returns:
        str: The SQL code for the WHERE clause.
    """
    if condition is None or condition == '':
        return ''
    condition = ' AND '.join(condition) if isinstance(condition, (tuple, list)) else condition
    sql_str = WHERE.format(condition)
    return sql_str


def select(column_name: str | tuple | list, table_name: str | tuple | list, condition: str | tuple | list = None) -> str:
    """
    Generate SQL code to select data from a table.

    Args:
        column_name (str | tuple | list): The column to select.
        table_name (str | tuple | list): The table to select from.
        condition (str | tuple | list): The condition for the selection.

    Returns:
        str: The SQL code to select data from the table.
    """
    columns = ', '.join(column_name) if isinstance(column_name, (tuple, list)) else column_name
    tables = ', '.join(table_name) if isinstance(table_name, (tuple, list)) else table_name
    condition = where(condition)
    sql_str = SELECT.format(columns, tables, condition)
    return sql_str.strip()


def insert(table_name: str, column_name: str | tuple | list, value) -> str:
    """
    Generate SQL code to insert data into a table.

    Args:
        table_name (str): The table to insert data into.
        column_name (str | tuple | list): The column to insert data into.
        value: The value to insert.

    Returns:
        str: The SQL code to insert data into the table.
    """
    if not check_size(column_name, value):
        raise ValueError("column_names and values must have the same length")
    columns = ', '.join(column_name) if isinstance(column_name, (tuple, list)) else column_name
    value = process_value(value)
    value = ', '.join(value) if isinstance(value, list) else value
    sql_str = INSERT.format(table_name, columns, value)
    return sql_str


def update(table_name: str, column_name: str | tuple | list, value, condition: str | tuple | list = None) -> str:
    """
    Generate SQL code to update data in a table.

    Args:
        table_name (str): The table to update data in.
        column_name (str | tuple | list): The column to update.
        value: The value to update.
        condition (str | tuple | list): The condition for the update.

    Returns:
        str: The SQL code to update data in the table.
    """
    if not check_size(column_name, value):
        raise ValueError("column_names and values must have the same length")
    value = process_value(value)
    set_clause = ', '.join(f"{col} = {val}" for col, val in zip(column_name, value)) if isinstance(column_name, (tuple, list)) else f"{column_name} = {value}"
    condition = where(condition)
    sql_str = UPDATE.format(table_name, set_clause, condition)
    return sql_str.strip()


def delete(table_name: str, condition: str | tuple | list = None) -> str:
    """
    Generate SQL code to delete data from a table.

    Args:
        table_name (str): The table to delete data from.
        condition (str | tuple | list): The condition for the deletion.

    Returns:
        str: The SQL code to delete data from the table.
    """
    condition = where(condition)
    sql_str = DELETE.format(table_name, condition)
    return sql_str.strip()


def like(pattern: str) -> str:
    """
    Generate SQL code for a LIKE condition.

    Args:
        pattern (str): The pattern to match.

    Returns:
        str: The SQL code for the LIKE condition.
    """
    sql_str = LIKE.format(pattern)
    return sql_str


def union(query1: str, query2: str) -> str:
    """
    Generate SQL code for a UNION operation.

    Args:
        query1 (str): The first query.
        query2 (str): The second query.

    Returns:
        str: The SQL code for the UNION operation.
    """
    sql_str = UNION.format(query1, query2)
    return sql_str


def order_by(column_name: str, ascending: bool = True) -> str:
    """
    Generate SQL code for an ORDER BY clause.

    Args:
        column_name (str): The column to order by.
        ascending (bool): Whether to order in ascending or descending order.

    Returns:
        str: The SQL code for the ORDER BY clause.
    """
    order = 'ASC' if ascending else 'DESC'
    sql_str = ORDER_BY.format(f"{column_name} {order}")
    return sql_str


def group_by(column_name: str | tuple | list) -> str:
    """
    Generate SQL code for a GROUP BY clause.

    Args:
        column_name (str | tuple | list): The column to group by.

    Returns:
        str: The SQL code for the GROUP BY clause.
    """
    columns = ', '.join(column_name) if isinstance(column_name, (tuple, list)) else column_name
    sql_str = GROUP_BY.format(columns)
    return sql_str


def join(table1: str, table2: str, join_type: str = 'INNER', condition: str | tuple | list = None) -> str:
    """
    Generate SQL code for a JOIN operation.

    Args:
        table1 (str): The first table.
        table2 (str): The second table.
        join_type (str): The type of join (INNER, LEFT, RIGHT).
        condition (str | tuple | list): The condition for the join.

    Returns:
        str: The SQL code for the JOIN operation.
    """
    if join_type not in ['INNER', 'LEFT', 'RIGHT', 'NATURAL']:
        raise ValueError(f"Unsupported join type: {join_type}")
    if condition is None:
        condition = ''
    else:
        condition = ' AND '.join(condition) if isinstance(condition, (tuple, list)) else condition
        condition = 'ON ' + condition
    sql_str = JOIN.format(table1, join_type, table2, condition)
    return sql_str.strip()


def add_column(table_name: str, column_name: str, data_type: str) -> str:
    """
    Generate SQL code to add a column to a table.

    Args:
        table_name (str): The name of the table.
        column_name (str): The column to add.
        data_type (str): The data type of the column.

    Returns:
        str: The SQL code to add the column.
    """
    if data_type not in DTYPE_MAPPING:
        raise ValueError(f"Unsupported data type: {data_type}")
    sql_str = ADD_COLUMN.format(table_name, column_name, DTYPE_MAPPING[data_type])
    return sql_str


def drop_column(table_name: str, column_name: str) -> str:
    """
    Generate SQL code to drop a column from a table.

    Args:
        table_name (str): The name of the table.
        column_name (str): The column to drop.

    Returns:
        str: The SQL code to drop the column.
    """
    sql_str = DROP_COLUMN.format(table_name, column_name)
    return sql_str


def modify_column(table_name: str, column_name: str, data_type: str) -> str:
    """
    Generate SQL code to modify a column in a table.
    Args:
        table_name (str): The name of the table.
        column_name (str): The column to modify.
        data_type (str): The new data type of the column.
    Returns:
        str: The SQL code to modify the column.
    """
    if data_type not in DTYPE_MAPPING:
        raise ValueError(f"Unsupported data type: {data_type}")
    sql_str = MODIFY_COLUMN.format(table_name, column_name, DTYPE_MAPPING[data_type])
    return sql_str


def rename_column(table_name: str, old_name: str, new_name: str, data_type: str) -> str:
    """
    Generate SQL code to rename a column in a table.
    Args:
        table_name (str): The name of the table.
        old_name (str): The current name of the column.
        new_name (str): The new name of the column.
        data_type (str): The data type of the column.
    Returns:
        str: The SQL code to rename the column.
    """
    if data_type not in DTYPE_MAPPING:
        raise ValueError(f"Unsupported data type: {data_type}")
    sql_str = RENAME_COLUMN.format(table_name, old_name, new_name, DTYPE_MAPPING[data_type])
    return sql_str


def add_primary_key(table_name: str, column_name: str | tuple | list) -> str:
    """
    Generate SQL code to add a primary key to a table.
    Args:
        table_name (str): The name of the table.
        column_name (str | tuple | list): The column to set as primary key.
    Returns:
        str: The SQL code to add the primary key.
    """
    columns = ', '.join(column_name) if isinstance(column_name, (tuple, list)) else column_name
    sql_str = ADD_PRIMARY_KEY.format(table_name, columns)
    return sql_str


def add_foreign_key(table_name: str, column_name: str, ref_table: str, ref_column: str) -> str:
    """
    Generate SQL code to add a foreign key to a table.
    Args:
        table_name (str): The name of the table.
        column_name (str): The column to set as foreign key.
        ref_table (str): The referenced table.
        ref_column (str): The referenced column.
    Returns:
        str: The SQL code to add the foreign key.
    """
    sql_str = ADD_FOREIGN_KEY.format(table_name, column_name, ref_table, ref_column)
    return sql_str


def rename_table(old_name: str, new_name: str) -> str:
    """
    Generate SQL code to rename a table.
    Args:
        old_name (str): The current name of the table.
        new_name (str): The new name of the table.
    Returns:
        str: The SQL code to rename the table.
    """
    sql_str = RENAME_TABLE.format(old_name, new_name)
    return sql_str


def create_database(db_name: str) -> str:
    """
    Generate SQL code to create a database.
    Args:
        db_name (str): The name of the database.
    Returns:
        str: The SQL code to create the database.
    """
    sql_str = CREATE_DATABASE.format(db_name)
    return sql_str


def drop_database(db_name: str) -> str:
    """
    Generate SQL code to drop a database.
    Args:
        db_name (str): The name of the database.
    Returns:
        str: The SQL code to drop the database.
    """
    sql_str = DROP_DATABASE.format(db_name)
    return sql_str


def use_database(db_name: str) -> str:
    """
    Generate SQL code to use a database.
    Args:
        db_name (str): The name of the database.
    Returns:
        str: The SQL code to use the database.
    """
    sql_str = USE_DATABASE.format(db_name)
    return sql_str