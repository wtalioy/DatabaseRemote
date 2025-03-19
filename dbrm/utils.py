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