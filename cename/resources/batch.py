from cename.resources.base import BaseResource
from cename import db
from cename.models import Batch
import json
import logging


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
        temp = []
        if batch_no:
            try:
                logging.info("Getting a batch")
                temp = Batch.query.get(batch_no).jsonify(detailed=True)
            except Exception as e:
                logging.error(str(e))
        else:
            logging.info("Getting all batches")
            temp = [bat.jsonify(detailed=True) \
                    for bat in Batch.query.all() ]
        return temp


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
                        logging.error(str(e))
                        return {"messsage": "Unable to update batch at the moment"}, 500
                try:
                    db.session.commit()
                except Exception as e:
                    logging.error(str(e))
                    db.session.rollback()
                    return {"message": "Unable to update the batch at the moment"}, 500

                logging.info("Batch updated successfully")
                return {"message": "batch updated successfully"}, 200
            else:
                logging.info("Invalid batch_no, batch not found")
                return {"message": "no such batch"}, 500
                
        else:
            logging.warning("No batch data given")
            return {"message": "no batch data recieved"}, 500

class Delete_batch(BaseResource):
    def __init__(self):
        super().__init__()

    def delete(self, batch_no=None):
        if batch_no:
            bat = Batch.query.get(batch_no)
            if bat:    
                try:
                    logging.info("Deleting batch")
                    db.session.delete(bat)
                    db.session.commit()
                except Exception as e:
                    logging.error(str(e))
                    db.session.rollback()
                    return {'message': "Internal Error while trying to delete"}, 500
                else:
                    logging.info("Batch deleted")
                    return {'message': "batch deleted successfully"}, 200
            else:
                logging.info(f"No batch found with the given batch_no {batch_no}")
                return {"message": "no such batch with batch_no '%s'"%(batch_no)}, 500
        else:
            logging.warning("No batch data given")
            return {'message': "no batch_no given "}, 500
