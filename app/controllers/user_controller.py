from flask import Blueprint, render_template, request, redirect, url_for
from ..models import User
from .. import db
from ..utils import format_date

user = Blueprint('user', __name__)


@user.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        position = request.form['position']
        department = request.form['department']
        date_started = format_date(request.form.get('date_started'))
        date_ended = None

        new_user = User(name=name,
                        role=role,
                        position=position,
                        department=department,
                        date_started=date_started,
                        date_ended=date_ended
                        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.users_list'))

    return render_template('users/add_user.html')


@user.route('/users-list')
def users_list():
    users = User.query.all()
    present_users = User.query.filter_by(date_ended=None).all()
    present_users_count = len(present_users)
    former_users = User.query.filter(User.date_ended.isnot(None)).all()
    former_users_count = len(former_users)
    return render_template('users/users_list.html',
                           users=users,
                           present_users=present_users,
                           present_users_count=present_users_count,
                           former_users=former_users,
                           former_users_count=former_users_count
                           )


@user.route('/update-user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.date_ended = format_date(request.form.get('date_ended'))

        db.session.commit()
        return redirect(url_for('user.users_list'))
    return render_template('users/update_user.html', user=user)


@user.route('/delete-user/<int:id>', methods=['POST'])
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('user.users_list'))
