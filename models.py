from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_number = db.Column(db.String(20), nullable=False)
    manual_date = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    edit_date = db.Column(db.DateTime)

    def formatted_date(self):
        return self.date.strftime('%d.%m.%Y %H:%M')