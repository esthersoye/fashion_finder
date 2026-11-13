import psycopg2
from getpass import getpass
from pathlib import Path

password = getpass("Enter your PostgreSQL password: ")

connection = psycopg2.connect(
    host="localhost",
    database="fashion_finder",
    user="postgres",
    password=password
)

cursor = connection.cursor()

sql_file = Path(__file__).parent / "create_tables.sql"

with open(sql_file, "r") as file:
    cursor.execute(file.read())

connection.commit()

cursor.close()
connection.close()

print("Tables created successfully.")