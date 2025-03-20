CREATE_DATABASE = "CREATE DATABASE {}" # name
USE_DATABASE = "USE {}" # name
DROP_DATABASE = "DROP DATABASE {}" # name
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS {} ({})" # name, column_info
DROP_TABLE = "DROP TABLE {}" # name
WHERE = "WHERE {}" # condition
SELECT = "SELECT {} FROM {} {}" # column, tables, condition
INSERT = "INSERT INTO {} ({}) VALUES ({})" # table, column, value
UPDATE = "UPDATE {} SET {} {}" # table, column, condition
DELETE = "DELETE FROM {} {}" # table, condition
LIKE = "LIKE '{}'" # pattern
UNION = "{} UNION {}" # query1, query2
ORDER_BY = "ORDER BY {}" # column-option
GROUP_BY = "GROUP BY {}" # column
JOIN = "{} {} JOIN {} {}" # table1, option(NATURAL|LEFT|RIGHT), table2, condition
ADD_COLUMN = "ALTER TABLE {} ADD COLUMN {} {}" # name, column, datatype
DROP_COLUMN = "ALTER TABLE {} DROP COLUMN {}" # name, column
MODIFY_COLUMN = "ALTER TABLE {} MODIFY COLUMN {} {}" # name, column, datatype
RENAME_COLUMN = "ALTER TABLE {} CHANGE COLUMN {} {} {}" # name, old_name, new_name, datatype
ADD_PRIMARY_KEY = "ALTER TABLE {} ADD PRIMARY KEY ({})" # name, column
ADD_FOREIGN_KEY = "ALTER TABLE {} ADD FOREIGN KEY ({}) REFERENCES {} ({})" # name, column, table, column
RENAME_TABLE = "ALTER TABLE {} RENAME TO {}" # old_name, new_name

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