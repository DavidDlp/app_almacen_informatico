from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user

# DataBase
from db import Base, engine, db_session
# Models
from models.products import Product
from models.user.forms import RegisterForm, LoginForm
from models.user.users import User, addInitialUser, addAdmin
from models.roles import addRole


# Inicio servidor Flask
app = Flask(__name__)

# Configuración
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'abcdefg1234567'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    id = User.query.get(id)
    print(id)
    return id

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
    # if request.method == 'POST':
    #     print(request.form['username'])
    #     print(request.form['password'])
    return render_template("login.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, name=form.name.data)
        db_session.add(new_user)
        db_session.commit()
        db_session.close()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route('/home')
@login_required
def home():
    all_products = db_session.query(Product).all()
    return render_template("index.html", all_products=all_products)

if __name__ == '__main__':
    Base.metadata.drop_all(bind=engine, checkfirst=True)

    Base.metadata.create_all(engine)
    Product.addInitialProducts()
    addRole()
    addAdmin()
    addInitialUser()

    app.run(debug=True)


