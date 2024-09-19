from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product
from . import db

main = Blueprint('main', __name__)


# Home route
@main.route('/')
def home():
    return render_template('home_page.html')


# Add a new product
@main.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('main.inventory'))
    return render_template('add_product.html')


# List all items in inventory
@main.route('/inventory/all')
def inventory():
    items = Product.query.all()
    return render_template('inventory.html', items=items)


# List items by category
@main.route('/inventory/<category>')
def list_inventory(category):
    items = Product.query.filter_by(category=category).all()
    return render_template('inventory_list.html', items=items, category=category)


# Update product status
@main.route('/update_status/<int:id>', methods=['GET', 'POST'])
def update_status(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.status = request.form['status']
        product.assigned_to = request.form.get('assigned_to', None)
        db.session.commit()
        return redirect(url_for('main.inventory'))
    return render_template('update_status.html', product=product)


# Delete product
@main.route('/delete_item/<int:id>', methods=['POST'])
def delete_item(id):
    item_to_delete = Product.query.get_or_404(id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('main.inventory'))


# Dashboard overview
@main.route('/dashboard')
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
