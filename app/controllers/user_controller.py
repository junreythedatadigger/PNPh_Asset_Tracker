from flask import Blueprint, render_template, request, redirect, url_for
from ..models import User
from .. import db
from ..utils import format_date, format_boolean

user = Blueprint('user', __name__)


@user.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        position = request.form['position']
        date_started = request.form['date_started']
        has_ended = request.form.get('has_ended')
        date_ended = request.form.get('date_ended')

        if date_started:
            date_started = format_date(date_started)

        has_ended = format_boolean(has_ended)

        if has_ended:
            date_ended = format_date(date_ended)
        else:
            date_ended = None

        new_user = User(name=name,
                        role=role,
                        position=position,
                        date_started=date_started,
                        has_ended=has_ended,
                        date_ended=date_ended
                        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.users_list'))

    return render_template('add_user.html')


@user.route('/users-list')
def users_list():
    users = User.query.all()
    return render_template('users_list.html', users=users)


@user.route('/delete-user/<int:id>', methods=['POST'])
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('user.users_list'))
