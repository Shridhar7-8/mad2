from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from sqlalchemy import or_,func
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
from flask_cors import CORS
from flask_login import LoginManager, login_user,current_user,logout_user, login_required,UserMixin
from flask_restful import Resource, Api,fields, marshal_with, reqparse

#----------------------------------------- Configurations -------------------------------------------------#

app = Flask(__name__)
api = Api(app)
app.secret_key = 'shridharpiyush'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shridhar.sqlite3"
db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)

CORS(app)

#------------------------------------------ Models -----------------------------------------------#

class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    admin_name = db.Column(db.String, unique=True, nullable=False)
    contact_no = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    sections = db.relationship('Section', backref='admin', lazy=True)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    section_type = db.Column(db.String(50))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=False)

    products = db.relationship('Product', backref='section', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacture_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime)
    rate = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    available_stock = db.Column(db.Integer, default=0)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('sales', lazy=True))


#-------------------------------------------------------------------------------------------------#
with app.app_context():
    db.create_all()

@login_manager.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    else:
        return render_template('home.html')

@app.route('/user_login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        
        return redirect(url_for('user_dashboard'))
    if request.method=='GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        user = User.query.filter(User.username==username,User.password==password).first()

        if user:
            
            session['user_id'] = user.id
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username/password', 'error')
            return redirect(url_for('login'))

    
@app.route('/user/create/', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 3 or len(username) > 50:
            flash("Username must be between 3 and 50 characters")
            return render_template('create_user.html')
        if not re.match("^[A-Za-z][A-Za-z0-9_.]*$", username):
            flash("Username must have only letters, numbers, dots or underscores")
            return render_template('create_user.html')
        
        
        if len(password) < 8:
            flash("Password must be at least 8 characters")
            return render_template('create_user.html')
        
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("user created Successfully!")
        return redirect(url_for('login'))

    
@app.route('/logout')
@login_required
def logout():
    
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/admin_logout')
def adminlogout():

    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        pswd = request.form['password']
        admin = Admin.query.filter(Admin.admin_name==admin_name, Admin.password==pswd).first()
        if admin:
            
            session['admin_id'] = admin.admin_id
            return redirect(url_for('admindashboard'))
        else:
            flash('Invalid username/password', 'error')
            return redirect(url_for('admin'))



    
@app.route('/admin/create/', methods=['GET','POST'])
def createadmin():
    if request.method == 'GET':
        return render_template('createadmin.html')
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        pswd = request.form['password']
        contact = request.form['contact_no']

        if len(admin_name) < 3 or len(admin_name) > 50:
            flash("Username must be between 3 and 50 characters")
            return render_template('createadmin.html')
        if not re.match("^[A-Za-z][A-Za-z0-9_.]*$", admin_name):
            flash("Username must have only letters, numbers, dots or underscores")
            return render_template('createadmin.html')
        
        
        if len(pswd) < 8:
            flash("Password must be at least 8 characters")
            return render_template('createadmin.html')
        
        if not re.match("^[0-9]{10}$", contact):
            flash("Contact number must be a valid 10-digit number")
            return render_template('createadmin.html')
        
        admin = Admin(admin_name=admin_name,contact_no=contact,password=pswd)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('admin'))
    
@app.route('/admin/section/create/', methods=['GET', 'POST'])
def create_section():
    if request.method == 'GET':
        return render_template('create_section.html')
    if request.method == 'POST':
        name = request.form['name']
        section_type = request.form['section_type']

        
        admin_id = session.get('admin_id')

        existing_section = Section.query.filter_by(name=name).first()

        if existing_section:
            flash('A section with that name already exists!', 'warning')
            return redirect(url_for('create_section'))
        else:
            section = Section(name=name, section_type=section_type, admin_id=admin_id)
            db.session.add(section)
            db.session.commit()

            flash('Section created successfully!', 'success')
            return redirect(url_for('admindashboard'))

    
@app.route('/admin/dashboard/')
def admindashboard():
    sections = Section.query.all()
    products=Product.query.all()
    return render_template('admindashboard.html', sections=sections,products=products)

    
@app.route('/admin/section/edit/<int:section_id>/', methods=['GET', 'POST'])
def edit_section(section_id):
    if request.method == 'GET':
        section=Section.query.get_or_404(section_id)
        return render_template('edit_section.html',section=section)
    
    if request.method == 'POST':
        section=Section.query.get_or_404(section_id)
        section.name = request.form['name']
        section.section_type = request.form['section_type']
        db.session.commit()
        
        flash('Section updated successfully!', 'success')
        return redirect(url_for('admindashboard'))

@app.route('/admin/section/delete/<int:section_id>/', methods=['GET', 'POST'])
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)

    if request.method == 'GET':
        return render_template('delete_section.html', section=section)

    if request.method == 'POST':
        if 'confirm_delete' in request.form and request.form['confirm_delete'] == 'true':
            Product.query.filter_by(section_id=section.id).delete()
            db.session.delete(section)
            db.session.commit()

            flash('Section deleted successfully!', 'success')
        else:
            flash('Deletion canceled!', 'warning')

        return redirect(url_for('admindashboard'))



@app.route('/admin/section/view/<int:section_id>/')
def view_section(section_id):
    section = Section.query.get_or_404(section_id)
    products = Product.query.filter_by(section_id=section_id).all()
    return render_template('view_section.html', section=section, products=products)



@app.route('/admin/product/create/', methods=['GET', 'POST'])
def create_product():
    if request.method == 'GET':
        sections = Section.query.all()
        return render_template('create_product.html', sections=sections)
    if request.method == 'POST':
        name = request.form['name']
        manufacture_date = datetime.strptime(request.form['manufacture_date'], '%Y-%m-%d')
        expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d')
        rate = float(request.form['rate'])
        unit = request.form['unit']
        available_stock = request.form['available_stock']
        section_id = int(request.form['section'])

        existing_product = Product.query.filter_by(name=name).first()

        if existing_product:
            flash('A product with that name already exists!', 'warning')
            return redirect(url_for('create_product'))
        else:
            product = Product(name=name, manufacture_date=manufacture_date, expiry_date=expiry_date,
                          rate=rate, unit=unit,available_stock=available_stock, section_id=section_id)
            db.session.add(product)
            db.session.commit()

            flash('Product created successfully!', 'success')
            return redirect(url_for('admindashboard'))
    
@app.route('/admin/product/edit/<int:product_id>/', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'GET':
        sections = Section.query.all()
        return render_template('edit_product.html', product=product, sections=sections)
    if request.method == 'POST':
        product.name = request.form['name']
        product.manufacture_date = datetime.strptime(request.form['manufacture_date'], '%Y-%m-%d')
        product.expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d')
        product.rate = float(request.form['rate'])
        product.unit = request.form['unit']
        product.available_stock = request.form['available_stock']
        product.section_id = int(request.form['section'])

        db.session.commit()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('admindashboard'))
    
@app.route('/admin/product/delete/<int:product_id>/', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'GET':
        return render_template('delete_product.html', product=product)

    if request.method == 'POST':
        if 'confirm_delete' in request.form and request.form['confirm_delete'] == 'true':
            # Check if the product is present in any user's cart
            cart_items_with_product = CartItem.query.filter_by(product_id=product.id).all()

            if cart_items_with_product:
                flash('Cannot delete the product as it is present in users\' carts!', 'danger')
            else:
                # Find and remove any associated Sales items
                sales_items = Sale.query.filter_by(product_id=product.id).all()
                for sale_item in sales_items:
                    db.session.delete(sale_item)

                db.session.delete(product)
                db.session.commit()

                flash('Product deleted successfully!', 'success')
        else:
            flash('Deletion canceled!', 'warning')

        return redirect(url_for('admindashboard'))

    
@app.route('/user_dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    if request.method == 'POST' and 'logout' in request.form:
        session.clear()
        flash('Logged out successfully!', 'success')
        return redirect(url_for('user_login'))
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_name = user.username

    sections = Section.query.all()  

    
    return render_template('user_dashboard.html', sections=sections,user_name=user_name)



@app.route('/categories', methods=['GET', 'POST'])
def categories():
    sections = Section.query.all()

    search_query = request.form.get('search_query', '') 

    if search_query:
        sections = Section.query.filter(Section.name.ilike(f"%{search_query}%")).all()

    return render_template('categories.html', sections=sections, search_query=search_query)


@app.route('/category/<int:section_id>/products')
def products(section_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_name = user.username

    section = Section.query.get(section_id)
    products = Product.query.filter_by(section_id=section_id).all()
    return render_template('products.html', section=section, products=products,user_name=user_name)

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    product = Product.query.get(product_id)

    if product and product.available_stock >= quantity:
        total_price = quantity * product.rate

        if 'user_id' in session:
            user_id = session['user_id']

            
            product.available_stock -= quantity
            db.session.commit()

            
            cart_item = CartItem.query.filter_by(product_id=product_id, user_id=user_id).first()
            if cart_item:
                
                cart_item.quantity += quantity
                db.session.commit()
            else:
            
                cart_item = CartItem(product_id=product_id, quantity=quantity, user_id=user_id)
                db.session.add(cart_item)
                db.session.commit()

            flash('Product added to cart successfully!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('User not logged in!', 'error')
            return redirect(url_for('login'))
    else:
        flash('out of stock!', 'warning')
        return redirect(url_for('user_dashboard'))



@app.route('/cart')
def cart():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_name = user.username
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total_price = sum(item.product.rate * item.quantity for item in cart_items if item.product)


    return render_template('cart.html', cart_items=cart_items, total_price=total_price,user_name=user_name)


@app.route('/remove_from_cart/<int:cart_item_id>', methods=['GET', 'POST'])
@login_required
def remove_from_cart(cart_item_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_name = user.username

    cart_item = CartItem.query.get_or_404(cart_item_id)

    if request.method == 'GET':
        return render_template('remove_from_cart.html', cart_item=cart_item,user_name=user_name)

    if request.method == 'POST':
        if 'confirm_delete' in request.form and request.form['confirm_delete'] == 'true':
            quantity = cart_item.quantity
            product = cart_item.product
            product.available_stock += quantity

            db.session.delete(cart_item)
            db.session.commit()

            flash('Item removed from cart successfully!', 'success')
        else:
            flash('Removal canceled!', 'warning')

        return redirect(url_for('user_dashboard'))
    
@app.route('/edit_cart_item/<int:cart_item_id>', methods=['GET', 'POST'])
@login_required
def edit_cart_item(cart_item_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_name = user.username

    cart_item = CartItem.query.get_or_404(cart_item_id)

    if request.method == 'POST':
        quantity = int(request.form['quantity'])

        quantity_change = quantity - cart_item.quantity
        
        cart_item.quantity = quantity
        
        cart_item.product.available_stock -= quantity_change

        db.session.commit()

        flash('Cart item updated successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('edit_cart_item.html', cart_item=cart_item,user_name=user_name)



@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_name = user.username

    query = request.form.get('query')

    
    if query and query.strip():
        products = Product.query.filter(
            or_(
                Product.name.ilike(f'%{query}%'),
                Product.manufacture_date.ilike(f'%{query}%'),
                Product.rate.ilike(f'%{query}%')
            )
        ).all()
    else:
        products = []

    return render_template('search_results.html', products=products,user_name=user_name)

@app.route('/buy_cart_items', methods=['GET', 'POST'])
@login_required
def buy_cart_items():
    user_id = session.get('user_id')

    if request.method == 'GET':
        
        return render_template('buy_cart_items.html')

    if request.method == 'POST':
        if 'confirm_buy' in request.form and request.form['confirm_buy'] == 'true':
            
            cart_items = CartItem.query.filter_by(user_id=user_id).all()

            for item in cart_items:
                sale = Sale(product_id=item.product_id, quantity=item.quantity)
                db.session.add(sale)
                db.session.delete(item)

            db.session.commit()

            flash('Cart items bought successfully!', 'success')
        else:
            flash('Purchase canceled!', 'warning')

        return redirect(url_for('user_dashboard'))




@app.route('/summary')
def summary():
    
    section_counts = db.session.query(Section.name, func.count(Product.id)).join(Product).group_by(Section.name).all()

    # a bar chart for the number of items in each section
    section_names = [section[0] for section in section_counts]
    section_item_counts = [section[1] for section in section_counts]
    plt.bar(section_names, section_item_counts)
    plt.title('Number of Items in Each Section')
    plt.xlabel('Section')
    plt.ylabel('Number of Items')
    plt.savefig('static/section_counts.png')
    plt.clf()

    
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    sales_counts_by_section = db.session.query(Section.name, func.sum(Sale.quantity)).select_from(Section).join(Product).join(Sale).filter(Sale.date >= seven_days_ago).group_by(Section.name).all()

    # a bar chart for the number of items sold from each section
    section_names = [sale[0] for sale in sales_counts_by_section]
    section_sales_counts = [sale[1] for sale in sales_counts_by_section]
    plt.bar(section_names, section_sales_counts)
    plt.title('Number of Items Sold from Each Section in the Past Seven Days')
    plt.xlabel('Section')
    plt.ylabel('Number of Items Sold')
    plt.savefig('static/sales_counts_by_section.png')
    plt.clf()

    
    sales_counts = db.session.query(Product.name, func.sum(Sale.quantity)).join(Sale).filter(Sale.date >= seven_days_ago).group_by(Product.name).all()

    # a bar chart for the number of individual products sold
    product_names = [sale[0] for sale in sales_counts]
    product_sales_counts = [sale[1] for sale in sales_counts]
    plt.bar(product_names, product_sales_counts)
    plt.title('Number of Individual Products Sold in the Past Seven Days')
    plt.xlabel('Product')
    plt.ylabel('Number of Items Sold')
    plt.savefig('static/sales_counts.png')
    plt.clf()

    return render_template('summary.html')

#---------------------------------------------------------------------------------------------------------------#

# API Parsers
section_parse = reqparse.RequestParser()
section_parse.add_argument("name", required=True, help="Section Name is required")
section_parse.add_argument("section_type")

product_parse = reqparse.RequestParser()
product_parse.add_argument("name", required=True, help="Product Name is required")
product_parse.add_argument("manufacture_date", type=lambda x: datetime.strptime(x, "%Y-%m-%d").date(), default=datetime.utcnow().date)
product_parse.add_argument("expiry_date", type=lambda x: datetime.strptime(x, "%Y-%m-%d").date(), required=False)
product_parse.add_argument("rate", type=float, required=True, help="Rate is required")
product_parse.add_argument("unit", required=True, help="Unit is required")
product_parse.add_argument("section_id", type=int, required=True, help="Section ID is required")
product_parse.add_argument("available_stock", type=int, default=0)

#---------------------------------------------------------------------------------------------------------------#

# Output Fields
section_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "section_type": fields.String,
    "admin_id": fields.Integer
}

product_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "manufacture_date": fields.DateTime(dt_format='iso8601'),
    "expiry_date": fields.DateTime(dt_format='iso8601'),
    "rate": fields.Float,
    "unit": fields.String,
    "section_id": fields.Integer,
    "available_stock": fields.Integer
}

#------------------------------------------------------------------------------------------------------------------#

# API Resources
class SectionAPI(Resource):
    @marshal_with(section_fields)
    def get(self, section_id=None): 
        if section_id is None:
            sections = Section.query.all()
            return sections
        else:
            section = Section.query.get(section_id)
            if section:
                return section
            else:
                return {"message": "Section not found"}, 404

    @marshal_with(section_fields)
    def put(self, section_id):
        section = Section.query.get(section_id)
        if section:
            args = section_parse.parse_args()
            section.name = args["name"]
            section.section_type = args["section_type"]
            db.session.commit()
            return section
        else:
            return {"message": "Section not found"}, 404

    def delete(self, section_id):
        section = Section.query.get(section_id)
        if section:
            # Delete the section and its associated products
            products_to_delete = Product.query.filter_by(section_id=section_id).all()
            for product in products_to_delete:
                db.session.delete(product)
            db.session.delete(section)
            db.session.commit()
            return {"message": "Section deleted successfully"}, 200
        else:
            return {"message": "Section not found"}, 404

    @marshal_with(section_fields)
    def post(self):
        args = section_parse.parse_args()
        name = args["name"]
        section_type = args["section_type"]
        admin_id = 1  # Replace with the actual admin_id value
        section = Section(name=name, section_type=section_type, admin_id=admin_id)
        db.session.add(section)
        db.session.commit()
        return section, 201

class ProductAPI(Resource):
    @marshal_with(product_fields)
    def get(self, product_id=None):
        if product_id is None:
            products = Product.query.all()
            return products
        else:
            product = Product.query.get(product_id)
            if product:
                return product
            else:
                return {"message": "Product not found"}, 404
    @marshal_with(product_fields)
    def put(self, product_id):
        product = Product.query.get(product_id)
        if product:
            args = product_parse.parse_args()
            product.name = args["name"]
            product.manufacture_date = args["manufacture_date"]
            product.expiry_date = args["expiry_date"]
            product.rate = args["rate"]
            product.unit = args["unit"]
            product.section_id = args["section_id"]
            product.available_stock = args["available_stock"]
            db.session.commit()
            return product
        else:
            return {"message": "Product not found"}, 404

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product deleted successfully"}, 200
        else:
            return {"message": "Product not found"}, 404

    @marshal_with(product_fields)
    def post(self):
        args = product_parse.parse_args()
        name = args["name"]
        manufacture_date = args["manufacture_date"]
        expiry_date = args["expiry_date"]
        rate = args["rate"]
        unit = args["unit"]
        section_id = args["section_id"]
        available_stock = args["available_stock"]
        section = Section.query.get(section_id)
        if not section:
            return {"message": "Section not found"}, 404
        product = Product(
            name=name,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            rate=rate,
            unit=unit,
            section_id=section_id,
            available_stock=available_stock
        )
        db.session.add(product)
        db.session.commit()
        return product, 201

#-----------------------------------------------------------------------------------------------------------------#


api.add_resource(SectionAPI, "/api/sections/<int:section_id>", "/api/sections")
api.add_resource(ProductAPI, "/api/products/<int:product_id>", "/api/products")

#-----------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=True)

#------------------------------------------------------------------------------------------------------------------#