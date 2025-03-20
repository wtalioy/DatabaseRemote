"""
Utility functions for data processing and SQL query generation.
"""

DTYPE_MAPPING = {
    # Pandas numeric types
    'int64': 'INTEGER',
    'int32': 'INTEGER',
    'int16': 'INTEGER',
    'int8': 'INTEGER',
    'uint64': 'INTEGER',
    'uint32': 'INTEGER',
    'uint16': 'INTEGER',
    'uint8': 'INTEGER',
    'float64': 'DOUBLE',
    'float32': 'FLOAT',
    'float16': 'FLOAT',
    # Python native types
    'int': 'INTEGER',
    'float': 'FLOAT',
    'bool': 'BOOLEAN',
    'str': 'VARCHAR(255)',
    # Pandas/NumPy date types
    'datetime64[ns]': 'DATETIME',
    'datetime64': 'DATETIME',
    'timedelta64': 'INTERVAL',
    'datetime': 'DATETIME',
    'date': 'DATE',
    # Pandas/Python string and categorical types
    'object': 'VARCHAR',
    'category': 'VARCHAR(255)',
    'text': 'TEXT',
    # Additional types
    'dict': 'JSON',
    'list': 'JSON',
    'complex': 'VARCHAR(255)',
    'bytes': 'BLOB',
    'bytearray': 'BLOB',
}

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