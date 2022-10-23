from flask import Flask, render_template, request, redirect, url_for
import db
from models.products import Product

# Inicio servidor Flask
app = Flask(__name__)

@app.route('/')
def home():
    all_products = db.session.query(Product).all()
    for item in all_products:
        print(item)
    return render_template("index.html", all_products=all_products)

if __name__ == '__main__':
    db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)

    db.Base.metadata.create_all(db.engine)
    Product.addInitialProducts()

    app.run(debug=True)


