from cename.resources.base import BaseResource
from cename import db
from cename.models import Distribution, Region, Batch
import json
import logging


# Table of content
# -----------------
# ... 1. Get distribution
# ... 2. Make distribution


class Get_distribution(BaseResource):
    def __init__(self):
        super().__init__()

    def get(self, region_code=None):
        if region_code:
            # if the request is for a particular row
            logging.info("Getting distributions for a region")
            region = Region.query.get(region_code) 
            if region:
                logging.info("Region found, getting distributions")
                query = region.distributions
                response = self.parse_query(query)
            else:
                logging.info(f"Invalid region_code given {region_code}")
                return {"message": "invalid region_code '%s'"%(region_code)}, 500
        else:
            # else get all the tables
            logging.info("Getting all distributions")
            query = Distribution.query.all()
            response = self.parse_query(query)

        return response, 200


class Make_distribution(BaseResource):
    def __init__(self):
        super().__init__()

    def post(self):
        data = self.get_request_data()
        if data != "":
            try:
                logging.info("About to make a distribution")
                data = self.convert_data_to_dict(data)
                check = self.validate_transaction(data)
                if check['ok']:
                    logging.info("Transaction reprocessing and validation ok")
                    db.session.add(Distribution(**data))
                    Batch.query.get(data['batch_no']).available -= int(data['quantity'])
                    db.session.commit()
                    logging.info("Transaction successfull")
                    return {'message': "Transaction successfull"}, 200
                else:
                    logging.info("Transaction validation failed")
                    return check['msg'], 500
            except Exception as e:
                logging.error(str(e))
                return {"message" : "Internal or Update Error"}, 500
        else:
            logging.warning("No data given")
            return {"message": "no data passed"}, 500

    @staticmethod
    def check_batch_quantity(batch, qty):
        if int(qty) < batch.available:
            return True
        return False

    def validate_transaction(self, transaction_data):
        """
        Verify and validate a distribution.
        Steps:
            1. Verify if the batch exists
            2. Verify if the quantity in the batch is enough
            3. verify if the region exists
        """
        batch = Batch.query.get(transaction_data['batch_no'])
        if batch:
            if self.check_batch_quantity(batch, transaction_data['quantity']):
                if Region.query.get(transaction_data['region_code']):
                    return {'ok': True, 'msg': ''}
                else:
                    logging.info("Invalid region_code")
                    return {'ok': False, 'msg': 'Invalid region. Operation failed'}    
            else:
                logging.info("Invalid quantity")
                return {'ok': False, 'msg': 'Invalid transaction quantity. Operation failed'}
        else:
            logging.info("Invalid batch_no")
            return {'ok': False, 'msg': "No such batch. Operation failed"}