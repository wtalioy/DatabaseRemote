from pandas import DataFrame
from typing import Literal
from itertools import islice
import dbrm.sqlinterpreter as itp
from dbrm.utils import DTYPE_MAPPING

class SQLTable:
    def __init__(
        self,
        cursor,
        table_name: str,
        dataframe: DataFrame | None = None,
        if_exists: Literal["append", "replace", "fail"] = "fail",
    ):
        self.cursor = cursor
        self.name = table_name
        self.data = dataframe
        self.dtypes = self._get_dtypes()
        self.if_exists = if_exists

    def exists(self) -> bool:
        try:
            # Simple query that will fail if table doesn't exist
            self.cursor.execute(f"SELECT 1 FROM {self.name} LIMIT 1")
            return True
        except Exception:
            return False

    def _get_dtypes(self) -> list:
        dtypes = []
        for col in self.data.columns:
            dtype = self.data[col].dtype
            dtype_name = dtype.name if hasattr(dtype, 'name') else str(dtype)
            
            if dtype_name == "object" and self.data[col].notna().any():
                length = self.data[col].str.len().max()
                if length > 255:
                    dtype_name = "text"
            dtype = DTYPE_MAPPING[dtype_name]
            dtypes.append(dtype)
        return dtypes
    
    def _execute_create(self) -> None:
        sql_str = itp.create_table(self.name, self.data.columns.tolist(), self.dtypes)
        self.cursor.execute(sql_str)
        self.cursor.commit()

    def create(self) -> None:
        if self.exists():
            if self.if_exists == "fail":
                raise ValueError(f"Table '{self.name}' already exists.")
            if self.if_exists == "replace":
                drop_sql = itp.drop_table(self.name)
                self.cursor.execute(drop_sql)
                self.cursor.commit()
                self._execute_create()
            elif self.if_exists == "append":
                pass
            else:
                raise ValueError(f"'{self.if_exists}' is not valid for if_exists")
        else:
            self._execute_create()

    def _execute_insert(self, column_names: list[str], data_iter) -> None:
        sql_template = itp.insert_many_template(self.name, column_names)
        self.cursor.executemany(sql_template, data_iter)
        self.cursor.commit()

    def insert(self, chunk_size: int | None = None) -> None:
        """
        Insert data from the dataframe into the table.
        
        Args:
            chunk_size (int, optional): Number of rows to insert at once. 
                                        If None, all rows are inserted in one go.
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data to insert.")
        
        nrows = len(self.data)
        if chunk_size is None or chunk_size < 0:
            chunk_size = nrows
        elif chunk_size == 0:
            raise ValueError("Chunk size cannot be zero.")
        column_names = self.data.columns.tolist()
        data_iter = self.data.itertuples(index=False, name=None)
        for _ in range(0, nrows, chunk_size):
            chunk = list(islice(data_iter, chunk_size))
            self._execute_insert(column_names, chunk)