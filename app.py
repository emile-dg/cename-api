import resource

from flask import Flask, request
from flask_restful import Api 
from flask_cors import CORS

from models import db, Region
from sys import argv

def start_app(_db=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()

    cors = CORS(app, resource={r'/*':{'origin': "*"}})

    return app, db

def prepare_db(db):
    """Prepare the database with necessary entries"""
    regions = {
            'ADA': 'ADAMAWA', 
            'CEN': 'CENTER', 
            'EST': 'EAST', 
            'FND': 'FAR NORTH', 
            'LIT': 'LITORAL',
            'NRD': 'NORD', 
            'NDW': 'NORD WEST', 
            'STH': 'SOUTH', 
            'STW': 'SOUTH WEST', 
            'WST': 'WEST'
        }
    for code in regions.keys():
        db.session.add(Region(region_code=code, region_name=regions[code]))
    db.session.commit()
    

def add_resources(api):
    api.add_resource(resource.Get_invoice, 
                    '/get/invoices',
                    '/get/invoice/<string:invoice_no>')
    api.add_resource(resource.Update_invoice,
                    '/update/invoice')
    api.add_resource(resource.Update_batch,
                    '/update/batch')
    api.add_resource(resource.Add_invoice,
                    '/add/invoice')
    api.add_resource(resource.Get_batches,
                    '/get/batches',
                    '/get/batch/<string:batch_no>')
    api.add_resource(resource.Get_regions,
                    "/get/regions")
    api.add_resource(resource.Make_distribution,
                    "/make/distribution")
    api.add_resource(resource.Get_distribution, 
                    '/get/distributions',
                    '/get/distribution/<string:region_code>')
                    

if __name__ == "__main__":

    app, db = start_app()
    api = Api(app)
    add_resources(api)

    if "--reset" in argv:
        print("- Resetting the database...")
        db.drop_all()
        db.create_all()
        prepare_db(db)

    app.run(debug=True, host="0.0.0.0", port=1909)
