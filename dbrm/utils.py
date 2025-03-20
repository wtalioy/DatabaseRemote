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
    'float64': 'FLOAT',
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


def get_column_info(df) -> tuple:
    """
    Get the data types and lengths of each column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        Tuple: A tuple of tuples containing the column name, data type, and length.
    """
    column_info = []
    for col in df.columns:
        dtype = df[col].dtype
        length = None
        if dtype == 'object' and df[col].notna().any():
            length = df[col].str.len().max()
            if length > 255:
                dtype = 'text'
                length = None
        column_info.append((col, dtype, length))
    return tuple(column_info)


def size(obj) -> int:
    return len(obj) if hasattr(obj, '__len__') and not isinstance(obj, str) else 1