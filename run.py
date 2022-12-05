import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from decimal import Decimal
# DataBase
from db import Base, engine, db_session
# Form
from forms.formUsers import RegisterFormUser, LoginForm
from forms.formProducts import RegisterFormProduct
from forms.formClient import ModifiedFormClient
from forms.formSupplier import ModifiedFormSupplier
# Models
from models.products import Product, addInitialProducts
from models.roles import addRole
from models.users import User, addInitialUser, addAdmin, addInitialSupplier
from models.orders import Order
from models.applyFor import Apply
from models.clients import Client
from models.suppliers import Supplier, addProfileInitialSupplier
# Servicies
from servicies.grafics import getProductMoreBuy, getProductMoreApplyFor

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
        # print(form.typeOfUser.data)
        db_session.add(new_user)
        db_session.commit()
        db_session.close()
        return redirect(url_for('login'))

    return render_template("user/register.html", form=form)

# Control Panel Admin
@app.route('/control-panel', methods=['GET', 'POST'])
def control_panel():
    #Todos los proveedores
    all_supplier = db_session.query(Supplier).all()

    #Todos mis productos
    my_product = db_session.query(Product).all()

    #Facturacion
    my_apply = []
    my_sales = []
    for product in my_product:
        my_apply.append(db_session.query(Apply).filter(Apply.product_id == product.id_product).all())
        my_sales.append(db_session.query(Order).filter(Order.product_id == product.id_product).all())

    all_apply = []
    all_sales = []
    total_amount = 0
    total_sales = 0

    for apply in my_apply:
        for item in apply:
            all_apply.append(item)
            product = db_session.query(Product).filter(Product.id_product == item.product_id).first()
            purchase_price = product.purchase_price
            total_amount += purchase_price * 10
            bills = float(total_amount) * 0.8

    for order in my_sales:
        for item in order:
            all_sales.append(item)
            product = db_session.query(Product).filter(Product.id_product == item.product_id).first()
            sale_price = product.sale_price
            total_sales += sale_price

    invoiced = float(total_sales) - bills

    return render_template("user/control_panel.html",  all_supplier=all_supplier,
                           bills=bills,
                           total_sales=total_sales,
                           invoiced=invoiced)

# Profile Client
@app.route('/profile-client', methods=['GET', 'POST'])
def profile_client():
    client_profile = db_session.query(Client).filter(Client.user_id == current_user.id).first()
    my_orders = db_session.query(Order).filter(Order.user_id == current_user.id).all()
    print(my_orders)
    if not client_profile:
        flash("Complete su perfil")
    return render_template('Client/profile-client.html', client_profile=client_profile, my_orders=my_orders)

@app.route('/edit-client', methods=['GET', 'POST'])
def edit_client():
    form = ModifiedFormClient()
    if form.validate_on_submit():
        user_id = current_user.id
        client = db_session.query(Client).filter(Client.user_id == user_id).first()
        if client is None:
            new_client = Client(name=form.name.data, lastname=form.lastname.data, address=form.address.data,
                                country=form.country.data, city=form.city.data,
                                cp=form.cp.data, phone=form.phone.data, user_id=user_id)
            db_session.add(new_client)
            db_session.commit()
            db_session.close()
            flash("Perfil creado correctamente")
        else:
            client.name = form.name.data
            client.lastname = form.lastname.data
            client.address = form.address.data,
            client.country = form.country.data
            client.city = form.city.data,
            client.cp = form.cp.data
            client.phone = form.phone.data,
            db_session.commit()
            db_session.close()
            flash("Perfil editado correctamente")

        return redirect(url_for('profile_client'))
    return render_template('Client/edit-client.html', form=form)

# Profile Supplier
@app.route('/profile-supplier', methods=['GET', 'POST'])
def profile_supplier():
    supplier_profile = db_session.query(Supplier).filter(Supplier.user_id == current_user.id).first()
    if not supplier_profile:
        return redirect(url_for('edit_supplier'))
    else:
        supplier_id = supplier_profile.id_supplier
        # print(supplier_id)
        # Productos del proveedor
        my_product = db_session.query(Product).filter(Product.supplier_id == supplier_id).all()
        # Facturacion
        my_apply = []
        for product in my_product:
            # print(product.id_product)
            my_apply.append(db_session.query(Apply).filter(Apply.product_id == product.id_product).all())
        all_apply = []
        total_amount = 0
        for apply in my_apply:
            for item in apply:
                all_apply.append(item)
                product = db_session.query(Product).filter(Product.id_product == item.product_id).first()
                supplier = db_session.query(Supplier).filter(Supplier.id_supplier == product.supplier_id).first()
                # discount_decimal = Decimal(supplier.discount / 100)
                # Tengo problemas en esta parte revisar.
                purchase_price = product.purchase_price
                total_amount += purchase_price * 10
                billing = float(total_amount) * 0.8
        # print(all_apply)
        number_apply = len(all_apply)
        # if not supplier_profile:
        #     flash("Complete su perfil")
        return render_template('supplier/profile-supp.html',
                        supplier_profile=supplier_profile,
                        my_product=my_product,
                        all_apply=all_apply, number_apply=number_apply,
                        total_amount=total_amount,
                        billing=billing)

@app.route('/edit-supplier', methods=['GET', 'POST'])
def edit_supplier():
    form = ModifiedFormSupplier()
    if form.validate_on_submit():
        user_id = current_user.id
        supplier = db_session.query(Supplier).filter(Supplier.user_id == user_id).first()
        if supplier is None:
            new_supplier = Supplier(company_name=form.company_name.data, country=form.country.data, user_id=user_id)
            db_session.add(new_supplier)
            db_session.commit()
            db_session.close()
            flash("Perfil creado correctamente")
        else:
            supplier.company_name = form.company_name.data
            country = form.country.data
            db_session.commit()
            db_session.close()
            flash("Perfil editado correctamente")
        return redirect(url_for('profile_supplier'))


    return render_template('supplier/edit-supplier.html',  form=form)

# Crud Product
@app.route('/create-product', methods=['GET', 'POST'])
def create_new_product():
    form = RegisterFormProduct()
    if form.validate_on_submit():
        # print(form.choices.data.id_supplier)
        new_product = Product(product_name=form.product_name.data, mark=form.mark_product.data,
                              type=form.type_product.data, sale_price=form.sale_price.data,
                              purchase_price=form.purchase_price.data,
                              description=form.description.data, supplier_id=form.choices.data.id_supplier)
        db_session.add(new_product)
        db_session.commit()
        db_session.close()
        return redirect(url_for('home'))
    return render_template('product/create-product.html', form=form)

# Order and Apply For
@app.route('/create-order/<id>', methods=['GET', 'POST'])
def create_order(id):
    product_id = id
    # print(product_id)
    product = db_session.query(Product).filter(Product.id_product == product_id).first()
    product.quantity -= 1
    user_id = current_user.id
    date = datetime.datetime.now()
    # print(user_id)
    order = Order(date, product_id, user_id)
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
    product.quantity += 10
    user_id = current_user.id
    date = datetime.datetime.now()
    # print(user_id)
    apply = Apply(date, product_id, user_id)
    db_session.add(apply)
    db_session.commit()
    db_session.close()
    print("Cantidad modificada con exito")
    print("Pedido al proveedor Realizado")
    flash("Pedido al proveedor realizada con exito")
    return redirect(url_for('home'))

# Servicies Routes
@app.route('/grafics')
def create_grafics():
    product = []
    if current_user.role_id == 2:
        dates = getProductMoreBuy()
        # for item in dates.index:
        #     print(dates["Product_Name"][item])
    else:
        dates = getProductMoreApplyFor()
    # print(dates)
    return render_template("grafics/grafics.html", dates=dates)

if __name__ == '__main__':
    # Base.metadata.drop_all(bind=engine, checkfirst=True)

    Base.metadata.create_all(engine)
    # addInitialProducts()
    # addRole()
    # addAdmin()
    # addInitialUser()
    # addInitialSupplier()
    # addProfileInitialSupplier()

    app.run(debug=True)


