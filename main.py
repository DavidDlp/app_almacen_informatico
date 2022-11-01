from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user

# DataBase
from db import Base, engine, session
# Models
from models.products import Product
from models.users import User, addInitialUser, addAdmin
from models.roles import addRole

# Inicio servidor Flask
app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/home')
def home():
    all_products = session.query(Product).all()
    return render_template("index.html", all_products=all_products)

if __name__ == '__main__':
    Base.metadata.drop_all(bind=engine, checkfirst=True)

    Base.metadata.create_all(engine)
    Product.addInitialProducts()
    addRole()
    addAdmin()
    addInitialUser()

    app.run(debug=True)


