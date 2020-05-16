"""
A simple utility script to fill the database with concrete data
NB: This utility is solely for testing purposes
"""
import json
from random import randint, randrange
import datetime
from tqdm import tqdm

from cename import db
from cename.models import Invoice, Batch


def commit_changes():
    """Apply the changes made to the database else raise an Exception"""
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def load_json_file(filename):
    with open("test/samples/%s"%(filename), "r") as f:
        return json.load(f)

def get_random_id(signature, generated_ids, tried=0):
    """
    Use of recursion to generate a random key which do not exist in a list 
    of keys with a limit of 10 failures i.e returns nothing if it generates 
    10 times keys which exist. Each time it generates a key, the key is 
    added to the list of used keys
    """
    x = randint(0, 1000)
    if x in generated_ids:
        if tried < 10:
            return get_random_id(signature, generated_ids, tried=tried+1)
        else:
            return None
    else:
        generated_ids.append(x)
    return signature+str(x).zfill(4)

def random_from(_list):
    return _list[randint(0, len(_list)-1)]

def random_date(s_date=datetime.date(2010, 1, 1),\
                e_date=datetime.date(2020, 12, 31)):
    delta = e_date - s_date
    dbd = delta.days # dbd = days betwwen dates
    random_no_days = randrange(dbd)
    return s_date + datetime.timedelta(days=random_no_days)

def generate_invoice_with_batch(no_invoice, batch_per_invoice=10):
    inv_data = {}
    batch_data = {}
    # --------------
    generated_inv_keys = []
    generated_bat_keys = []
    samples = load_json_file("invoices.json")
    # ----------------
    invoices_added = 0
    batches_added = 0
    counter = 0
    with tqdm(total=(no_invoice*batch_per_invoice)+no_invoice) as pbar:
        for i in range(no_invoice):
            # random values
            inv_data["invoice_no"] = get_random_id("INV", generated_inv_keys)
            inv_data["exporter"] = random_from(samples["exporters"])
            inv_data["stockage"] = random_from(samples['places'])
            inv_data["vessel"] = random_from(samples['vessels'])
            inv_data["delivery"] = random_from(samples['places'])
            inv_data["invoice_date"] = random_date()

            if inv_data['invoice_no'] != None:
                inv = Invoice(**inv_data)
                db.session.add(inv)
                invoices_added += 1
                pbar.update(1)
                for b in range(batch_per_invoice):
                    batch_data["batch_no"] = str(counter).zfill(5)
                    if batch_data['batch_no'] == None:
                        pbar.update(1)
                    else:
                        batch_data["invoice_no"] = inv.invoice_no
                        batch_data["num_of_ships"] = randint(1, 10)
                        batch_data["mfg_date"] = random_date(e_date=datetime.date(2013, 12, 31))
                        batch_data["exp_date"] = random_date(s_date=datetime.date(2015, 1, 1))
                        batch_data["description"] = "This is the description of the batch"
                        batch_data["quantity"] = randint(10, 500)
                        batch_data['available'] = batch_data['quantity'] * batch_data['num_of_ships']

                        batch = Batch(**batch_data)
                        db.session.add(batch)
                        batches_added += 1
                        pbar.update(1)
                        counter += 1
            commit_changes()

    inv_losess = no_invoice - invoices_added
    bat_losses = (batch_per_invoice * no_invoice) - batches_added

    print("Generated %d invoices with %d losses"%(invoices_added, inv_losess))
    print("Generated %d batches with %d losses"%(batches_added, bat_losses))

def start():
    i = int(input("number of invoices: "))
    b = int(input("number of batch per invoice: "))
    generate_invoice_with_batch(i, batch_per_invoice=b)

if __name__ == "__main__":
    start()