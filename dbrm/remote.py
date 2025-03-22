import pandas as pd
import numpy as np
from typing import Literal
from dbrm.dbconnector import get_cursor
from dbrm.sqltable import SQLTable


def transfer_csv(
    path: str,
    table_name: str,
    if_exists: Literal["append", "replace", "fail"] = "fail",
    chunk_size: int | None = None,
    **kwargs
) -> None:
    """
    Transfer a CSV file to a SQL table.

    Args:
        path (str): The path to the CSV file to transfer.
        table_name (str): The name of the SQL table.
        if_exists (Literal["append", "replace", "fail"]): What to do if the table already exists. Options are 'append', 'replace', or 'fail'.
        chunk_size (int | None): The number of rows to write at a time. If None, all rows will be written at once.
        **kwargs: Additional arguments for the SQL connection.

    Returns:
        None
    """
    cursor = get_cursor(**kwargs)
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("The CSV file is empty. No data to transfer.")
    sql_table = SQLTable(
        cursor=cursor,
        table_name=table_name,
        dataframe=df,
        if_exists=if_exists,
    )
    sql_table.create()
    sql_table.insert(chunk_size=chunk_size)