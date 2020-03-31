from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Invoice(db.Model):
    invoice_no = db.Column(db.String(50), primary_key=True)

    exporter = db.Column(db.String(50), nullable=False)
    stockage = db.Column(db.String(50), nullable=False)
    vessel = db.Column(db.String(50), nullable=False)
    delivery = db.Column(db.String(50), nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False)

    batches = db.relationship("Batch", backref="invoice",  cascade="all,delete", lazy=True)

    def jsonify(self):
        return {
            'invoice_no': self.invoice_no,
            'exporter': self.exporter,
            'stockage': self.stockage,
            'vessel': self.vessel,
            'delivery': self.delivery,
            'invoice_date': self.invoice_date.strftime("%m-%d-%y")
        }

class Batch(db.Model):
    batch_no = db.Column(db.String(10), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)
    num_of_ships = db.Column(db.Integer, nullable=False)
    mfg_date = db.Column(db.DateTime, nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text(500), nullable=False)

    invoice_no = db.Column(db.Integer, db.ForeignKey('invoice.invoice_no'), nullable=False)

    def jsonify(self):
        return {
            "batch_no" : self.batch_no,
            "quantity" : self.quantity,
            "num_of_ships" : self.num_of_ships,
            "mfg_date" : self.mfg_date.strftime("%m-%d-%y"),
            "exp_date" : self.exp_date.strftime("%m-%d-%y"),
            "description": self.description
        }

class Region(db.Model):
    region_code = db.Column(db.String(3), primary_key=True)
    region_name = db.Column(db.String(30), nullable=False)

    distributions = db.relationship("Distribution", backref=db.backref('region', cascade="all,delete", lazy=True))

    def jsonify(self):
        return {
            "region_code": self.region_code,
            "region_name": self.region_name
        }

class Distribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_code = db.Column(db.Integer, db.ForeignKey('region.region_code') )
    batch_no = db.Column(db.Integer, db.ForeignKey('batch.batch_no'))

    def jsonify(self):
        return {key:value for key, value in self.__dict__.items() if not key.startswith("__") and not callable(key)}


# class Region(db.Model):
#     region_id = db.Column(db.Integer, primary_key=True)
#     region_name = db.Column(db.String(150), unique=True, nullable=False)
#     invoices = db.relationship("Invoice", backref=db.backref('region', lazy=True))

#     def jsonify(self):
#         return {
#             'region_id': self.region_id,
#             'region_name': self.region_name
#         }