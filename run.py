from flask import Flask, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

# DataBase
from db import Base, engine, db_session
# Form
from forms.formUsers import RegisterFormUser, LoginForm
# Models
from models.products import Product, addInitialProducts
from models.roles import addRole
from models.users import User, addInitialUser, addAdmin, addInitialSupplier
from models.orders import Order
from models.applyFor import Apply


# Inicio servidor Flask
app = Flask(__name__)

# Configuración
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'abcdefg1234567'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    all_products = db_session.query(Product).all()
    return render_template("home.html", all_products=all_products)

# Login
@login_manager.user_loader
def load_user(id):
    id = User.query.get(id)
    # print(id)
    return id

@app.route('/login-user', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # print(user)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Wrong name or password...")
                return render_template("user/login.html", form=form)
        else:
            flash("Wrong name or password...")
            return render_template("user/login.html", form=form)
    return render_template("user/login.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Register User
@app.route('/register-user', methods=['GET', 'POST'])
def register():
    form = RegisterFormUser()
    if form.validate_on_submit():
        if form.typeOfUser.data == "Supplier":
            role = 3
        else:
            role = 2
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, role_id=role)
        print(form.typeOfUser.data)
        db_session.add(new_user)
        db_session.commit()
        db_session.close()
        return redirect(url_for('login'))

    return render_template("user/register.html", form=form)

# Register Supplier
@app.route('/register-supplier', methods=['GET', 'POST'])
def register_supplier():
    return render_template('user/reg-supplier.html')

# Crud Product
@app.route('/create-product', methods=['GET', 'POST'])
def create_new_product():
    return render_template('product/create-product.html')

# Order and Apply For
@app.route('/create-order/<id>', methods=['GET', 'POST'])
def create_order(id):
    product_id = id
    # print(product_id)
    product = db_session.query(Product).filter(Product.id_product == product_id).first()
    product.quantity -= 1
    user_id = current_user.id
    # print(user_id)
    order = Order(product_id, user_id)
    db_session.add(order)
    db_session.commit()
    db_session.close()
    print("Cantidad modificada con exito")
    print("Orden de compra CREADA")
    flash("Compra realizada con exito")
    return redirect(url_for('home'))

@app.route('/create-apply/<id>', methods=['GET', 'POST'])
def create_apply(id):
    product_id = id
    # print(product_id)
    product = db_session.query(Product).filter(Product.id_product == product_id).first()
    product.quantity += 1
    user_id = current_user.id
    # print(user_id)
    apply = Apply(product_id, user_id)
    db_session.add(apply)
    db_session.commit()
    db_session.close()
    print("Cantidad modificada con exito")
    print("Pedido al proveedor Realizado")
    flash("Pedido al proveedor realizada con exito")
    return redirect(url_for('home'))

if __name__ == '__main__':
    Base.metadata.drop_all(bind=engine, checkfirst=True)

    Base.metadata.create_all(engine)
    addInitialProducts()
    addRole()
    addAdmin()
    addInitialUser()
    addInitialSupplier()

    app.run(debug=True)


