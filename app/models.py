from . import db


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # IT device or Office furniture
    model = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(100), nullable=True)   # Serial number for IT Devices
    price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.Date, nullable=True)  # Optional: track purchase dates
    status = db.Column(db.String(50), nullable=False)  # Available, Unusable
    issuances = db.relationship('Issuance', backref='asset', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=True)
    date_started = db.Column(db.Date, nullable=False)
    has_ended = db.Column(db.Boolean, nullable=False, default=True)
    date_ended = db.Column(db.Date, nullable=True)
    count_asset_assigned = db.Column(db.Integer, nullable=False, default=0)
    issuances = db.relationship('Issuance', backref='user', lazy=True)


class Issuance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # date_issued = db.Column(db.String(20), nullable=False)
    date_issued = db.Column(db.Date, nullable=False)
    date_returned = db.Column(db.Date, nullable=True)


    def __repr__(self):
        return f"<Asset {self.name}>"
