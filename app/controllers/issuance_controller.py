from flask import Blueprint, render_template, request, redirect, url_for
from ..models import Issuance, Asset, User
from .. import db
import datetime
from ..utils import format_date

issuance = Blueprint('issuance', __name__)


@issuance.route('/add-issuance', methods=['GET', 'POST'])
def add_issuance():
    if request.method == 'POST':
        asset_id = request.form['asset_id']
        user_id = request.form['user_id']
        date_issued = format_date(request.form['date_issued'])
        
        new_issuance = Issuance(asset_id=asset_id, user_id=user_id, date_issued=date_issued)

        try:
            db.session.add(new_issuance)
            db.session.commit()
            return redirect(url_for('issuance.issuances_list'))
        except Exception as e:
            print(f"Error: {e}")
            return "There was an issue adding the issuance."

    # assets = Asset.query.all()
    # users = User.query.all()
    assets = Asset.query.filter_by(status='Available')
    users = User.query.filter_by(has_ended=False)

    return render_template('add_issuance.html', assets=assets, users=users)


@issuance.route('/issuances-list')
def issuances_list():
    issuances = Issuance.query.all()
    return render_template('issuances_list.html', issuances=issuances)


@issuance.route('/delete-issuance/<int:id>', methods=['POST'])
def delete_issuance(id):
    issuance_to_delete = Issuance.query.get_or_404(id)
    db.session.delete(issuance_to_delete)
    db.session.commit()
    return redirect(url_for('issuance.issuances_list'))
