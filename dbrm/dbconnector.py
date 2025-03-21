import pyodbc
import os
from dotenv import load_dotenv

def get_cursor():
    load_dotenv()
    
    connection_string = (
        f'DRIVER={os.getenv("DRIVER")};'
        f'SERVER={os.getenv("SERVER")};'
        f'DATABASE={os.getenv("DATABASE")};'
        f'UID={os.getenv("UID")};'
        f'PWD={os.getenv("PWD")};'
        'charset=utf8mb4;'
    )

    cnx = pyodbc.connect(connection_string)
    
    cnx.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
    cnx.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    cnx.setencoding(encoding='utf-8')
    
    cursor = cnx.cursor()
    return cursor

def get_db_connection():
    load_dotenv()
    
    connection_string = (
        f'DRIVER={os.getenv("DRIVER")};'
        f'SERVER={os.getenv("SERVER")};'
        f'DATABASE={os.getenv("DATABASE")};'
        f'UID={os.getenv("UID")};'
        f'PWD={os.getenv("PWD")};'
        'charset=utf8mb4;'
    )

    cnx = pyodbc.connect(connection_string)
    
    cnx.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
    cnx.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    cnx.setencoding(encoding='utf-8')
    
    return cnx
