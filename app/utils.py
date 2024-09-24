import datetime


def format_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()


def format_boolean(value):
    if value == 'yes':
        return True
    elif value is None:
        return False
