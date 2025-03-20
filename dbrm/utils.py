"""
Utility functions for data processing and SQL query generation.
"""

def size(obj) -> int:
    """
    Get the size of an object.
    Args:
        obj: The object to analyze.
    Returns:
        int: The size of the object.
    """
    if obj is None:
        return 0
    return len(obj) if hasattr(obj, '__len__') and not isinstance(obj, str) else 1


def check_size(obj1, obj2) -> bool:
    """
    Check if two objects are the same size.
    Args:
        obj1: The first object to compare.
        obj2: The second object to compare.
    Returns:
        bool: True if the objects are the same size, False otherwise.
    """
    return size(obj1) == size(obj2)


def to_sql_str(value) -> str:
    """
    Convert a value to a SQL string representation.
    Args:
        value: The value to convert.
    Returns:
        str: The SQL string representation of the value.
    """
    if isinstance(value, str):
        if len(value) == 0:
            return 'NULL'
        else:
            return f"'{value}'"
    else:
        return str(value)


def process_value(value) -> list | str:
    """
    Process a value for SQL queries.
    Args:
        value: The value to process.
    Returns:
        list | str: The processed value.
    """
    if isinstance(value, tuple) or isinstance(value, list):
        value = [to_sql_str(val) for val in value]
    else:
        value = to_sql_str(value)
    return value