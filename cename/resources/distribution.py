from cename.resources.base import BaseResource
from cename import db
from cename.models import Distribution, Region, Batch
import json


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
            region = Region.query.get(region_code) 
            if region:
                query = region.distributions
                response = self.parse_query(query)
            else:
                return {"message": "invalid region_code '%s'"%(region_code)}, 500
        else:
            # else get all the tables
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
                data = self.convert_data_to_dict(data)
                check = self.validate_transaction(data)
                if check['ok']:
                    db.session.add(Distribution(**data))
                    Batch.query.get(data['batch_no']).available -= int(data['quantity'])
                    db.session.commit()
                    return {'message': "Transaction successfull"}, 200
                else:
                    return check['msg'], 500
            except Exception as e:
                print(e)
                return {"message" : "Internal or Update Error"}, 500
        else:
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
                    return {'ok': False, 'msg': 'Invalid region. Operation failed'}    
            else:
                return {'ok': False, 'msg': 'Invalid transaction quantity. Operation failed'}
        else:
            return {'ok': False, 'msg': "No such batch. Operation failed"}