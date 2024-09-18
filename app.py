from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database (you can also use PostgreSQL, MySQL, etc.)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Product model for the database
class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # IT device or Office furniture
    status = db.Column(db.String(50), nullable=False)  # Available, Assigned, Unusable
    assigned_to = db.Column(db.String(100), nullable=True)  # Person assigned to if applicable
    purchase_date = db.Column(db.Date, nullable=True)  # Optional: track purchase dates
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    # comments = db.Column(db.String(100), nullable=True)  # Optional: Additional comments

    def __repr__(self):
        return f"<Product {self.name}>"


# Create the database
with app.app_context():
    db.create_all()


# Sample home route
@app.route('/')
def home():
    # return "Welcome to the Inventory System"
    return render_template('home_page.html')

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        status = request.form['status']
        assigned_to = request.form.get('assigned_to', None)
        quantity = request.form['quantity']
        price = request.form['price']
        new_product = Product(name=name, category=category, status=status, assigned_to=assigned_to, quantity=quantity, price=price)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_product.html')


# filter and list items by category
@app.route('/inventory/<category>')
def list_inventory(category):
    items = Product.query.filter_by(category=category).all()
    return render_template('inventory_list.html', items=items, category=category)


# change the status of an item
@app.route('/update_status/<int:id>', methods=['GET', 'POST'])
def update_status(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.status = request.form['status']
        product.assigned_to = request.form.get('assigned_to', None)
        db.session.commit()
        return redirect(url_for('list_inventory', category=product.category))
    return render_template('update_status.html', product=product)


# display an overview of inventory statistics
@app.route('/dashboard')
def dashboard():
    total_it_devices = Product.query.filter_by(category='IT Device').count()
    total_office_furniture = Product.query.filter_by(category='Office Furniture').count()

    total_available = Product.query.filter_by(status='Available').count()
    total_assigned = Product.query.filter_by(status='Assigned').count()
    total_unusable = Product.query.filter_by(status='Unusable').count()

    return render_template('dashboard.html',
                           total_it_devices=total_it_devices,
                           total_office_furniture=total_office_furniture,
                           total_available=total_available,
                           total_assigned=total_assigned,
                           total_unusable=total_unusable)


if __name__ == '__main__':
    app.run(debug=True)