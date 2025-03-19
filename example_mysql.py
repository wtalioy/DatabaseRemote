import mysql.connector
from config import MYSQL_CONFIG

cnx = mysql.connector.connect(
    host=MYSQL_CONFIG['host'],
    user=MYSQL_CONFIG['user'],
    password=MYSQL_CONFIG['password'],
    database=MYSQL_CONFIG['database'],
)

cursor = cnx.cursor()

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])