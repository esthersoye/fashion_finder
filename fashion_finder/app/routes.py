import os
import psycopg2
from flask import render_template
from app import app


def db_connect():
    return psycopg2.connect(
        database="fashion_finder",
        user="postgres",
        password=os.environ.get("PGPASSWORD"),
        host="localhost",
        port="5432"
    )



@app.route('/')
@app.route('/index')
def index():
    conn = db_connect()
    cur = conn.cursor()

    sql = """
        SELECT ItemID, ItemName, Price
        FROM clothing_item
        ORDER BY ItemID
    """

    cur.execute(sql)
    results = cur.fetchall()

    cur.close()
    conn.close()

    clothing_items = []

    for row in results:
        clothing_items.append({
            "id": row[0],
            "name": row[1],
            "price": row[2]
        })

    return render_template(
        "index.html",
        title="Home",
        clothing_items=clothing_items
    )



@app.route('/item/<int:item_id>')
def item_details(item_id):
    conn = db_connect()
    cur = conn.cursor()

    sql = """
        SELECT
            i.ItemName,
            i.Description,
            i.Price,
            b.BrandName,
            cat.CategoryName,
            s.SizeName,
            c.ColourName
        FROM clothing_item i
        JOIN brand b ON i.BrandID = b.BrandID
        JOIN category cat ON i.CategoryID = cat.CategoryID
        JOIN size s ON i.SizeID = s.SizeID
        JOIN colour c ON i.ColourID = c.ColourID
        WHERE i.ItemID = %s
    """

    cur.execute(sql, (item_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return "Clothing item not found", 404

    item = {
        "name": row[0],
        "description": row[1],
        "price": row[2],
        "brand": row[3],
        "category": row[4],
        "size": row[5],
        "colour": row[6]
    }

    return render_template(
        "item_details.html",
        title=item["name"],
        item=item
    )


@app.route('/about')
def about():
    return render_template(
        "about.html",
        title="About Us"
    )