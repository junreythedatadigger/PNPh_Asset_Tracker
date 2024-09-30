from flask import Blueprint, render_template, request, redirect, url_for
from ..models import Issuance, Asset, User
from .. import db
from ..utils import format_date

issuance = Blueprint('issuance', __name__)


@issuance.route('/add-issuance', methods=['GET', 'POST'])
def add_issuance():
    if request.method == 'POST':
        asset_id = request.form['asset_id']
        user_id = request.form['user_id']
        date_issued = format_date(request.form['date_issued'])
        remarks_on_issuance = request.form.get('remarks_on_issuance')
        date_returned = None
        remarks_on_returning = None

        # Update asset status to assigned
        asset = Asset.query.get_or_404(asset_id)
        asset.status = "Assigned"

        # Update the number of assets assigned to user by increasing count
        user = User.query.get_or_404(user_id)
        user.count_asset_assigned += 1
        
        new_issuance = Issuance(asset_id=asset_id,
                                user_id=user_id,
                                date_issued=date_issued,
                                remarks_on_issuance=remarks_on_issuance,
                                date_returned=date_returned,
                                remarks_on_returning=remarks_on_returning
                                )

        try:
            db.session.add(new_issuance)
            db.session.commit()
            return redirect(url_for('issuance.issuances_list'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an issue adding the issuance."

    assets = Asset.query.filter_by(status='Available')
    users = User.query.filter_by(date_ended=None)

    return render_template('issuances/add_issuance.html', assets=assets, users=users)


@issuance.route('/issuances-list')
def issuances_list():
    issuances = Issuance.query.all()
    return render_template('issuances/issuances_list.html', issuances=issuances)


@issuance.route('/update-issuance/<int:id>', methods=['GET', 'POST'])
def update_issuance(id):
    issuance = Issuance.query.get_or_404(id)
    if request.method == 'POST':
        issuance.date_returned = format_date(request.form['date_returned'])
        issuance.remarks_on_returning = request.form['remarks_on_returning']

        # Update asset status to available upon returning
        asset = Asset.query.get_or_404(issuance.asset.id)
        asset.status = 'Available'

        # Update the number of assets assigned to user by decreasing count
        user = User.query.get_or_404(issuance.user.id)
        user.count_asset_assigned -= 1

        db.session.commit()
        return redirect(url_for('issuance.issuances_list'))

    return render_template('issuances/update_issuance.html', issuance=issuance)


@issuance.route('/delete-issuance/<int:id>', methods=['POST'])
def delete_issuance(id):
    issuance_to_delete = Issuance.query.get_or_404(id)

    # Update asset status to available upon deleting
    asset = Asset.query.get_or_404(issuance_to_delete.asset.id)
    asset.status = 'Available'

    # Update the number of assets assigned to user by decreasing count upon deleting
    user = User.query.get_or_404(issuance_to_delete.user.id)
    user.count_asset_assigned -= 1

    db.session.delete(issuance_to_delete)
    db.session.commit()
    return redirect(url_for('issuance.issuances_list'))
