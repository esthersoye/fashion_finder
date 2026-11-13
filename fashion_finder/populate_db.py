import csv
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
data_folder = Path(__file__).parent / "data"

files = [
    (
        "brand.csv",
        """INSERT INTO brand (BrandID, BrandName)
        VALUES (%s, %s) ON CONFLICT (BrandID) DO NOTHING"""
    ),
    (
        "category.csv",
        """INSERT INTO category (CategoryID, CategoryName)
        VALUES (%s, %s) ON CONFLICT (CategoryID) DO NOTHING"""
    ),
    (
        "size.csv",
        """INSERT INTO size (SizeID, SizeName)
        VALUES (%s, %s) ON CONFLICT (SizeID) DO NOTHING"""
    ),
    (
        "colour.csv",
        """INSERT INTO colour (ColourID, ColourName)
        VALUES (%s, %s) ON CONFLICT (ColourID) DO NOTHING"""
    ),
    (
        "clothing_item.csv",
        """INSERT INTO clothing_item (
            ItemID, ItemName, Description, SizeID, ColourID,
            Price, ImageURL, BrandID, CategoryID
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ItemID) DO NOTHING"""
    )
]

for filename, query in files:
    with open(data_folder / filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row:
                cursor.execute(query, row)

connection.commit()
cursor.close()
connection.close()

print("Data added successfully.")
