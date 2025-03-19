import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
dsn = os.getenv('DSN')
user = os.getenv('DSN_USER')
pwd = os.getenv('DSN_PWD')
db = os.getenv('DB')

cnx = pyodbc.connect(f'DSN={dsn};UID={user};PWD={pwd};DATABASE={db}')

cursor = cnx.cursor()

query = "SHOW TABLES"
cursor.execute(query)

results = cursor.fetchall()
for row in results:
    print(row)