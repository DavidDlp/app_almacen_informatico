from flask import Flask, render_template, request, redirect, url_for
import db
from models.products import Product
from models.users import User
from models.roles import Role

# Inicio servidor Flask
app = Flask(__name__)


@app.route('/')
def home():
    all_products = db.session.query(Product).all()
    return render_template("index.html", all_products=all_products)

if __name__ == '__main__':
    db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)

    db.Base.metadata.create_all(db.engine)
    Product.addInitialProducts()
    Role.addRole()
    User.addAdmin()
    User.addInitialUser()

    app.run(debug=True)


