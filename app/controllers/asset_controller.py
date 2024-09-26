from flask import Blueprint, render_template, request, redirect, url_for# from ..models import Asset
from ..models import Asset
from .. import db
from ..utils import format_date

asset = Blueprint('asset', __name__)


@asset.route('/add-asset', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        asset_name = request.form['asset_name']
        category = request.form['category']
        model = request.form['model']
        serial_number = request.form['serial_number']
        price = request.form['price']
        purchase_date = request.form['purchase_date']
        status = request.form['status']

        if purchase_date:
            purchase_date = format_date(purchase_date)

        new_asset = Asset(asset_name=asset_name, category=category, model=model, serial_number=serial_number,
                          price=price, purchase_date=purchase_date, status=status)

        db.session.add(new_asset)
        db.session.commit()
        return redirect(url_for('asset.assets_list'))

    return render_template('assets/add_asset.html')


@asset.route('/assets-list')
def assets_list():
    items = Asset.query.all()
    return render_template('assets/assets_list.html', items=items)


@asset.route('/update-asset/<int:id>', methods=['GET', 'POST'])
def update_asset(id):
    asset = Asset.query.get_or_404(id)
    if request.method == 'POST':
        asset.status = request.form['status']
        db.session.commit()
        return redirect(url_for('asset.assets_list'))
    return render_template('assets/update_asset.html', asset=asset)


@asset.route('/delete-asset/<int:id>', methods=['POST'])
def delete_asset(id):
    asset_to_delete = Asset.query.get_or_404(id)
    db.session.delete(asset_to_delete)
    db.session.commit()
    return redirect(url_for('asset.assets_list'))
