CREATE_DATABASE = "CREATE DATABASE {}" # name
USE_DATABASE = "USE {}" # name
DROP_DATABASE = "DROP DATABASE {}" # name
CREATE_TABLE = "CREATE TABLE {} ({})" # name, column-datatype
DROP_TABLE = "DROP TABLE {}" # name
SELECT = "SELECT {} FROM {} WHERE {}" # columns, tables, conditions
INSERT = "INSERT INTO {} ({}) VALUES ({})" # table, columns, values
UPDATE = "UPDATE {} SET {} WHERE {}" # table, columns=values, conditions
DELETE = "DELETE FROM {} WHERE {}" # table, conditions
LIKE = "LIKE {}" # pattern
UNION = "{} UNION {}" # query1, query2
ORDER_BY = "ORDER BY {}" # column-option
GROUP_BY = "GROUP BY {}" # columns
JOIN = "{} {} JOIN {} ON {}" # table1, option(NATURAL|LEFT|RIGHT), table2, conditions
ADD_COLUMN = "ALTER TABLE {} ADD {} {}" # name, column, datatype
DROP_COLUMN = "ALTER TABLE {} DROP COLUMN {}" # name, column
MODIFY_COLUMN = "ALTER TABLE {} MODIFY {}" # name, column-datatype
RENAME_COLUMN = "ALTER TABLE {} CHANGE {} {} {}" # name, old_name, new_name, datatype
ADD_PRIMARY_KEY = "ALTER TABLE {} ADD PRIMARY KEY ({})" # name, columns
ADD_FOREIGN_KEY = "ALTER TABLE {} ADD FOREIGN KEY ({}) REFERENCES {} ({})" # name, column, table, column
RENAME_TABLE = "ALTER TABLE {} RENAME TO {}" # old_name, new_name