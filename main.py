from flask import Flask, render_template, request, redirect, url_for
import db
from models.products import Product
from models.users import User
from models.roles import Role

# Inicio servidor Flask
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/home')
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


