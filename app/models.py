from . import db


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # IT device or Office furniture
    model = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(100), nullable=True)   # Serial number for IT Devices
    price = db.Column(db.Float, nullable=False)
    # purchase_date = db.Column(db.Date, nullable=True)  # Optional: track purchase dates
    purchase_date = db.Column(db.String(20), nullable=True)  # Optional: track purchase dates
    status = db.Column(db.String(50), nullable=False)  # Available, Unusable


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    date_hired = db.Column(db.String(20), nullable=False)
    date_resigned = db.Column(db.String(20), nullable=True)
    # date_hired = db.Column(db.Date, nullable=False)
    # date_resigned = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Asset {self.name}>"
