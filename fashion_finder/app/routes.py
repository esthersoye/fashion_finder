import os
from decimal import Decimal, InvalidOperation

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import render_template, request
from app import app


@app.route('/')
@app.route('/index')
def index():
    selected_colour = request.args.get('colour', '').strip()
    max_price = request.args.get('max_price', '').strip()
    error = ''
    price_limit = None

    if max_price:
        try:
            price_limit = Decimal(max_price)

            if not price_limit.is_finite() or price_limit < 0:
                raise ValueError

        except (InvalidOperation, ValueError):
            error = 'Please enter a valid maximum price.'
            price_limit = None

    connection = psycopg2.connect(
        host='localhost',
        database='fashion_finder',
        user='postgres',
        password=os.environ.get('PGPASSWORD')
    )

    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                'SELECT ColourName FROM colour ORDER BY ColourID'
            )
            colours = [
                row['colourname'] for row in cursor.fetchall()
            ]

            query = """
                SELECT
                    i.ItemID AS id,
                    i.ItemName AS name,
                    i.Price AS price,
                    b.BrandName AS brand,
                    c.ColourName AS colour
                FROM clothing_item i
                JOIN brand b ON i.BrandID = b.BrandID
                JOIN colour c ON i.ColourID = c.ColourID
                WHERE 1 = 1
            """

            parameters = []

            if selected_colour:
                query += ' AND c.ColourName = %s'
                parameters.append(selected_colour)

            if price_limit is not None:
                query += ' AND i.Price <= %s'
                parameters.append(price_limit)

            query += ' ORDER BY i.ItemID'

            cursor.execute(query, parameters)
            clothing_items = cursor.fetchall()

    finally:
        connection.close()

    return render_template(
        'index.html',
        title='Home',
        clothing_items=clothing_items,
        colours=colours,
        selected_colour=selected_colour,
        max_price=max_price,
        error=error
    )


@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About Us'
    )