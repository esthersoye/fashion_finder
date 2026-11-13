from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    clothing_items = [
        {
            'name': 'Classic T-Shirt',
            'brand': 'Sample Brand A',
            'category': 'Tops',
            'size': 'M',
            'colour': 'White',
            'price': '19.99'
        },
        {
            'name': 'Straight Leg Jeans',
            'brand': 'Sample Brand B',
            'category': 'Jeans',
            'size': 'M',
            'colour': 'Blue',
            'price': '39.99'
        },
        {
            'name': 'Knitted Jumper',
            'brand': 'Sample Brand A',
            'category': 'Knitwear',
            'size': 'S',
            'colour': 'Black',
            'price': '29.99'
        }
    ]

    return render_template(
        'index.html',
        title='Home',
        clothing_items=clothing_items
    )


@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About Us'
    )