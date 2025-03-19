import pyodbc
from config import DSN_CONFIG

dsn = DSN_CONFIG['dsn']
user = DSN_CONFIG['user']
password = DSN_CONFIG['password']

connection = pyodbc.connect(f'DSN={dsn};UID={user};PWD={password};DATABASE=tinydp')

cursor = connection.cursor()

query = "SHOW TABLES"
cursor.execute(query)

results = cursor.fetchall()
for row in results:
    print(row)