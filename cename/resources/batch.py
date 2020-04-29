from cename.resources.base import BaseResource
from cename import db
from cename.models import Batch
import json


# Table of content
# -----------------
# ... 1. Get batch
# ... 2. Update batch
# ... 3. Delete batch


class Get_batches(BaseResource):
    def __init__(self):
        super().__init__()

    def get(self, batch_no=None):
        # if the batch_no is given then just fetch that
        # else then fetch all batches
        if batch_no:
           return self.fetch_from_db(Batch, batch_no), 200
        else:
            return self.fetch_from_db(Batch), 200


class Update_batch(BaseResource):
    def __init__(self):
        super().__init__()

    def put(self):
        data = self.get_request_data()
        if data != "":
            json_data = json.loads(data)
            batch_no = json_data['batch_no']
            
            _batch = Batch.query.get(batch_no)
            if _batch:
                for k in json_data.keys():
                    try:
                        if k != "batch_no":
                            if k.endswith("date"):
                                json_data[k] = self.convert_to_date(json_data[k])
                            setattr(_batch, k, json_data[k])
                    except Exception as e:
                        print(e)
                        return {"messsage": "Error while updating"}, 500
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    return {"message": "Error while updating the database. Probably internal."}, 500
                return {"message": "batch updated successfully"}, 200
            else:
                return {"message": "no such batch"}, 500
                
        else:
            return {"message": "no batch data recieved"}, 500

class Delete_batch(BaseResource):
    def __init__(self):
        super().__init__()

    def delete(self, batch_no=None):
        if batch_no:
            bat = Batch.query.get(batch_no)
            if bat:    
                try:
                    db.session.delete(bat)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    return {'message': "Internal Error while trying to delete"}, 500
                else:
                    return {'message': "batch deleted successfully"}, 200
            else:
                return {"message": "no such batch with batch_no '%s'"%(batch_no)}, 500
        else:
            return {'message': "no batch_no given "}, 500
