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
    created_on = db.Column(db.DateTime, default=datetime.now)
    last_update = db.Column(db.DateTime, default=datetime.now)

    batches = db.relationship("Batch", backref="invoice",  cascade="all,delete", lazy=True)

    def jsonify(self):
        return {
            'invoice_no': self.invoice_no,
            'exporter': self.exporter,
            'stockage': self.stockage,
            'vessel': self.vessel,
            'delivery': self.delivery,
            'invoice_date': "{0}-{1}-{2}".format(self.invoice_date.year,
                                                self.invoice_date.month,
                                                self.invoice_date.day)
        }

class Batch(db.Model):
    batch_no = db.Column(db.String(10), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)
    num_of_ships = db.Column(db.Integer, nullable=False)
    mfg_date = db.Column(db.DateTime, nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text(500), nullable=False)

    invoice_no = db.Column(db.String(50), db.ForeignKey('invoice.invoice_no'), nullable=False)

    def jsonify(self):
        return {
            "invoice_no": self.invoice_no,
            "batch_no" : self.batch_no,
            "quantity" : self.quantity,
            "num_of_ships" : self.num_of_ships,
            "mfg_date" : "{0}-{1}-{2}".format(self.mfg_date.year,
                                                self.mfg_date.month,
                                                self.mfg_date.day),
            "exp_date" : "{0}-{1}-{2}".format(self.exp_date.year,
                                                self.exp_date.month,
                                                self.exp_date.day),
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
    created_on = db.Column(db.DateTime, default=datetime.now)

    region_code = db.Column(db.Integer, db.ForeignKey('region.region_code') )
    batch_no = db.Column(db.Integer, db.ForeignKey('batch.batch_no'))

    def jsonify(self):
        return {
            'region_code': self.region_code,
            'batch_no': self.batch_no,
            'created_on': "{0}-{1}-{2}".format(self.created_on.year, self.created_on.month, self.created_on.day)
        }