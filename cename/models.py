from datetime import datetime
import json

from cename import db
from cename.utils import format_date


class Invoice(db.Model):
    invoice_no = db.Column(db.String(50), primary_key=True)

    exporter = db.Column(db.String(50), nullable=False)
    stockage = db.Column(db.String(50), nullable=False)
    vessel = db.Column(db.String(50), nullable=False)
    delivery = db.Column(db.String(50), nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)
    last_update = db.Column(db.DateTime, default=datetime.now)

    batches = db.relationship("Batch", backref="invoice",  single_parent=True, cascade="all, delete-orphan", lazy=True)

    def jsonify(self, details=None):
        response = {
            'invoice_no': self.invoice_no,
            'exporter': self.exporter,
            'stockage': self.stockage,
            'vessel': self.vessel,
            'delivery': self.delivery,
            'invoice_date': format_date(self.invoice_date),
            'created_on': format_date(self.created_on)
        }
        if details:
            if details == "low":
                response['batches'] = [batch.jsonify() for batch in self.batches]
            elif details == "high":
                response['batches'] = [batch.jsonify(detailed=True) for batch in self.batches]

        return response

    def __repr__(self):
        return json.dumps(self.jsonify())

class Batch(db.Model):
    batch_no = db.Column(db.String(10), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)
    num_of_ships = db.Column(db.Integer, nullable=False)
    mfg_date = db.Column(db.DateTime, nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text(500), nullable=False)

    distributions = db.relationship("Distribution", backref=db.backref('batch', cascade="all, delete", lazy=True))
    invoice_no = db.Column(db.String(50), db.ForeignKey('invoice.invoice_no'), nullable=False)

    def jsonify(self, detailed=False):
        result = {
            "invoice_no": self.invoice_no,
            "batch_no" : self.batch_no,
            "quantity" : self.quantity,
            "num_of_ships" : self.num_of_ships,
            "available" : self.available,
            "mfg_date" : format_date(self.mfg_date),
            "exp_date" : format_date(self.exp_date),
            "description": self.description
        }
        
        if detailed:
            result["distributions"] = [dist.jsonify() 
                                        for dist in self.distributions]
            result["distribution count"] = len(result['distributions'])
            result["distribution quantity"] = sum([dist.quantity for dist in self.distributions])

        return result

class Region(db.Model):
    region_code = db.Column(db.String(3), primary_key=True)
    region_name = db.Column(db.String(30), nullable=False)

    distributions = db.relationship("Distribution", \
                    backref=db.backref('region', cascade="all, delete", \
                    lazy=True))

    def jsonify(self, detailed=False):
        result = {
            "region_code": self.region_code,
            "region_name": self.region_name
        }
        if detailed:
            result['distributions'] = [dist.jsonify() \
                                        for dist in self.distributions]
        return result

class Distribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.now)

    region_code = db.Column(db.Integer, db.ForeignKey('region.region_code') )
    batch_no = db.Column(db.Integer, db.ForeignKey('batch.batch_no'))
    quantity = db.Column(db.Integer, nullable=False)

    def jsonify(self):
        return {
            'region_code': self.region_code,
            'batch_no': self.batch_no,
            'quantity': self.quantity,
            'created_on': format_date(self.created_on)
        }
