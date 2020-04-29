from cename.resources.base import BaseResource
from cename import db
from cename.models import Invoice, Batch
from datetime import datetime
import json

# Table of content
# -----------------
# ... 1. Get invoice
# ... 2. Add invoice
# ... 3. Update invoice
# ... 4. Delete invoice

class Get_invoice(BaseResource):
    def __init__(self):
        super().__init__()

    def get(self, invoice_no=None):
        temp = []
        if invoice_no:
            try:
                temp = Invoice.query.get(invoice_no).jsonify(details="high")
            except Exception as e:
                print(e)
                temp = []
        else:
            temp = [{**invoice.jsonify(details="low")} \
                    for invoice in Invoice.query.all()]
        return temp


class Add_invoice(BaseResource):
    def __init__(self):
        super().__init__()

    def missing_args(self):
        if self.get_request_data() == "":
            return True
        return False
    
    def post(self):
        if self.missing_args():
            return {'message': "Sorry but 'data' argument value is missing!"}, 500
        else:
            json_data = self.convert_data_to_dict(self.get_request_data())
            invoice_data = json_data['invoice_data']
            batches_data = json_data['batches']

            if len(batches_data) > 0:
                if not self.row_exist(Invoice, invoice_data['invoice_no']):
                    invoice_no = self.add_invoice(invoice_data)
                    for batch in batches_data:
                        if not self.row_exist(Batch, batch['batch_no']):
                            self.add_batch(batch, invoice_no)
                        else:
                            return {'message': "Cannot add batch. Duplicate 'batch_no' '%s'"%(batch['batch_no'])}, 500
                    return {'message': "Invoice and batche(s) added successfully!"}, 200
                else:
                    return {'message': "Cannot add Invoice. Duplicate 'invoice_no' '%s'"%(invoice_data['invoice_no'])}, 500
            else:
                return {'message': "No batch data recieved. Cannot add invoice"}, 500

    @staticmethod
    def convert_data_to_dict(raw_json):
        """Convert the data argument value into a python dictionary"""
        return json.loads(raw_json)

    def add_invoice(self, invoice_dict):
        invoice_dict['invoice_date'] = self.convert_to_date(invoice_dict['invoice_date'])
        inv = Invoice(**invoice_dict)
        db.session.add(inv)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error while updating the database. Probably internal."}, 500
        finally:
            return inv.invoice_no


    def add_batch(self, batch_dic, invoice_no):
        batch_dic['exp_date'] = self.convert_to_date(batch_dic['exp_date'])
        batch_dic['mfg_date'] = self.convert_to_date(batch_dic['mfg_date'])
        batch_dic['invoice_no'] = invoice_no

        db.session.add(Batch(**batch_dic))
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message": "Error while updating the database. Probably internal."}, 500

    def row_exist(self, model, pk):
        if model.query.get(pk):
            return True
        return False

class Update_invoice(BaseResource):
    def __init__(self):
        super().__init__()
        self.arguments_list = []
        self.init_args()
        self.args = self.parse_args()

    def put(self):
        data = self.get_request_data()
        if data != "":
            json_data = json.loads(data)
            invoice_no = json_data['invoice_no']
            
            inv = Invoice.query.get(invoice_no)
            if inv:
                for k in json_data.keys():
                    try:
                        if k.endswith("date") or k == 'created_on':
                            json_data[k] = self.convert_to_date(json_data[k])
                        try:
                            getattr(inv, k)
                            setattr(inv, k, json_data[k])
                            inv.last_update = datetime.now()
                            db.session.commit()
                            print(json_data)
                        except AttributeError:
                            return {"message": "Invalid attribute: %s"%(k)}, 500
                    except:
                        db.session.rollback()
                        return {"messsage": "Error while updating"}, 500
                    else:
                        return {"message": "invoice updated successfully"}, 200
            else:
                return {"message": "no such invoice"}, 500
        else:
            return {"message": "no invoice data recieved"}, 500

class Delete_invoice(BaseResource):
    def __init__(self):
        super().__init__()

    def delete(self, invoice_no=None):
        if invoice_no:
            inv = Invoice.query.get(invoice_no)
            if inv:    
                try:
                    db.session.delete(inv)
                    db.session.commit()
                except:
                    db.session.rollback()
                    return {'message': "Internal Error while trying to delete"}, 500
                else:
                    return {'message': "invoice deleted successfully"}, 200
            else:
                return {"message": "no such invoice with invoice_no '%s'"%(invoice_no)}, 500
        else:
            return {'message': "no invoice_no given "}, 500
