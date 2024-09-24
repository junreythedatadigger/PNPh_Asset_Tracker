from flask import Blueprint, render_template
from ..models import Asset

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
def home():
    return render_template('home_page.html')


@dashboard.route('/dashboard')
def dashboard_view():
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
