from flask import Blueprint, render_template, request, redirect, url_for
from .models import Asset, User
from . import db

main = Blueprint('main', __name__)


# Home route
@main.route('/')
def home():
    return render_template('home_page.html')


# Add a new product
@main.route('/add-asset', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        asset_name = request.form['asset_name']
        category = request.form['category']
        model = request.form['model']
        serial_number = request.form['serial_number']
        price = request.form['price']
        purchase_date = request.form.get('purchase_date', None)
        status = request.form['status']
        new_asset = Asset(asset_name=asset_name,
                          category=category,
                          model=model,
                          serial_number=serial_number,
                          price=price,
                          purchase_date=purchase_date,
                          status=status)
        db.session.add(new_asset)
        db.session.commit()
        return redirect(url_for('main.assets_list'))
    return render_template('add_asset.html')

@main.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        position = request.form['position']
        date_hired = request.form['date_hired']
        date_resigned = request.form['date_resigned']
        new_user = User(name=name,
                        role=role,
                        position=position,
                        date_hired=date_hired,
                        date_resigned=date_resigned)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.users_list'))
    return render_template('add_user.html')


# List of all assets
@main.route('/assets-list')
def assets_list():
    items = Asset.query.all()
    return render_template('assets_list.html', items=items)


# List of all users
@main.route('/users-list')
def users_list():
    users = User.query.all()
    return render_template('users_list.html', users=users)

# List items by category
@main.route('/inventory/<category>')
def list_inventory(category):
    items = Asset.query.filter_by(category=category).all()
    return render_template('inventory_list.html', items=items, category=category)


# Update product status
@main.route('/update_status/<int:id>', methods=['GET', 'POST'])
def update_status(id):
    asset = Asset.query.get_or_404(id)
    if request.method == 'POST':
        asset.status = request.form['status']
        asset.assigned_to = request.form.get('assigned_to', None)
        db.session.commit()
        return redirect(url_for('main.assets_list'))
    return render_template('update_status.html', asset=asset)


# Delete an asset
@main.route('/delete-asset/<int:id>', methods=['POST'])
def delete_asset(id):
    asset_to_delete = Asset.query.get_or_404(id)
    db.session.delete(asset_to_delete)
    db.session.commit()
    return redirect(url_for('main.assets_list'))


# Delete a user
@main.route('/delete-user/<int:id>', methods=['POST'])
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('main.users_list'))

# Dashboard overview
@main.route('/dashboard')
def dashboard():
    total_it_devices = Asset.query.filter_by(category='IT Device').count()
    total_office_furniture = Asset.query.filter_by(category='Office Furniture').count()

    total_available = Asset.query.filter_by(status='Available').count()
    total_assigned = Asset.query.filter_by(status='Assigned').count()
    total_unusable = Asset.query.filter_by(status='Unusable').count()

    return render_template('dashboard.html',
                           total_it_devices=total_it_devices,
                           total_office_furniture=total_office_furniture,
                           total_available=total_available,
                           total_assigned=total_assigned,
                           total_unusable=total_unusable)
