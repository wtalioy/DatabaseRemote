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
    cursor = cnx.cursor()
    return cursor
