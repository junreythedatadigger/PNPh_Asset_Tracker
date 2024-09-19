from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # IT device or Office furniture
    status = db.Column(db.String(50), nullable=False)  # Available, Assigned, Unusable
    assigned_to = db.Column(db.String(100), nullable=True)  # Person assigned to if applicable
    purchase_date = db.Column(db.Date, nullable=True)  # Optional: track purchase dates
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"
