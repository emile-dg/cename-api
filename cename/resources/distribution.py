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
            json_data = json.loads(data)
            region_code = json_data['region_code']
            batch_no = json_data['batch_no']
            
            region = Region.query.get(region_code)
            if region:
                bat = Batch.query.get(batch_no)
                if bat:
                    dist = Distribution(region_code=region.region_code, batch_no=bat.batch_no)
                    db.session.add(dist)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                        return {"message": "Error while updating the database. Probably internal."}, 500
                    else:
                        return {"message": "distribution added successfully"}, 200

                else:
                    return {'message': "invalid batch_no '%s'"%(batch_no)}, 500

            else:
                return {"message": "invalid region_code '%s'"%(region_code)}, 500
    
        else:
            return {"message": "no data passed"}, 500
