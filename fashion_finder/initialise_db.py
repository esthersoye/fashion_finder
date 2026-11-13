import psycopg2
from getpass import getpass
from pathlib import Path

password = getpass("Enter your PostgreSQL password: ")

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password=password
)

connection.autocommit = True
cursor = connection.cursor()

cursor.execute(
    "SELECT 1 FROM pg_database WHERE datname = %s",
    ("fashion_finder",)
)

if cursor.fetchone() is None:
    cursor.execute("CREATE DATABASE fashion_finder")
    print("Database created successfully.")
else:
    print("Database already exists.")

cursor.close()
connection.close()

connection = psycopg2.connect(
    host="localhost",
    database="fashion_finder",
    user="postgres",
    password=password
)

cursor = connection.cursor()

sql_file = Path(__file__).parent / "create_tables.sql"

with open(sql_file, "r", encoding="utf-8") as file:
    cursor.execute(file.read())

connection.commit()

cursor.close()
connection.close()

print("Tables created successfully.")