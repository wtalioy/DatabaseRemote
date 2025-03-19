import mysql.connector
import os

pwd = os.environ.get("MYSQL_PASSWORD")

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password=pwd,
    database='test',
)

cursor = cnx.cursor()

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])