from flask import Blueprint, render_template, request, redirect, url_for
from ..models import Asset
from .. import db
from ..utils import format_date

asset = Blueprint('asset', __name__)


@asset.route('/add-asset', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        asset_name = request.form['asset_name']
        category = request.form['category']
        type = request.form['type']
        model = request.form['model']
        serial_number = request.form['serial_number']
        price = request.form['price']
        purchase_date = request.form.get('purchase_date')
        status = 'Available' # default value for status

        if purchase_date:
            purchase_date = format_date(purchase_date)
        else:
            purchase_date = None

        new_asset = Asset(asset_name=asset_name,
                          category=category,
                          type=type,
                          model=model,
                          serial_number=serial_number,
                          price=price,
                          purchase_date=purchase_date,
                          status=status)

        db.session.add(new_asset)
        db.session.commit()
        return redirect(url_for('asset.assets_list'))

    return render_template('assets/add_asset.html')


@asset.route('/assets-list')
def assets_list():
    assigned_assets = Asset.query.filter_by(status='Assigned').all()
    assigned_assets_count = len(assigned_assets)
    available_assets = Asset.query.filter_by(status='Available').all()
    available_assets_count = len(available_assets)
    unusable_assets = Asset.query.filter_by(status='Unusable').all()
    unusable_assets_count = len(unusable_assets)
    all_assets = Asset.query.all()
    all_assets_count = len(all_assets)
    return render_template('assets/assets_list.html',
                           assigned_assets=assigned_assets,
                           assigned_assets_count=assigned_assets_count,
                           available_assets=available_assets,
                           available_assets_count=available_assets_count,
                           unusable_assets=unusable_assets,
                           unusable_assets_count=unusable_assets_count,
                           all_assets=all_assets,
                           all_assets_count=all_assets_count
                           )


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
