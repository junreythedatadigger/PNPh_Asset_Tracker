from flask import Blueprint, render_template
from ..models import Asset, User, Issuance

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard')
def dashboard_view():

    total_assets = Asset.query.count()
    total_users = User.query.count()
    available_assets = Asset.query.filter_by(status="Available").count()
    unusable_assets = Asset.query.filter_by(status="Unusable").count()

    return render_template('dashboards/dashboard.html',
                           total_assets = total_assets,
                           total_users = total_users,
                           available_assets = available_assets,
                           unusable_assets = unusable_assets
                           )
