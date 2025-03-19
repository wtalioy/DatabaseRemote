import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PWD')
db = os.getenv('DB')

cnx = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=db,
)

cursor = cnx.cursor()

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])