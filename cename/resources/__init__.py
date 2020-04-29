
from cename.resources.base import Get_regions
from cename.resources.invoice import Get_invoice, Add_invoice, Update_invoice, Delete_invoice
from cename.resources.batch import Get_batches, Update_batch, Delete_batch
from cename.resources.distribution import Make_distribution, Get_distribution

from cename import api

# -------------------------
#  bind reources to routes
# -------------------------

# ---------- GET ROUTES -----------------------
api.add_resource(Get_regions, '/get/regions')

api.add_resource(Get_invoice,   '/get/invoices', \
                                '/get/invoice/<string:invoice_no>')

api.add_resource(Get_batches,   '/get/batches', \
                                '/get/batch/<string:batch_no>')

api.add_resource(Get_distribution,  '/get/distributions', \
                                    '/get/distribution/<string:region_code>') 

# --------- UPDATE ROUTES -------------------
api.add_resource(Update_invoice, '/update/invoice')
api.add_resource(Update_batch, '/update/batch')

# -------- ADD ROUTES --------------- 
api.add_resource(Add_invoice, '/add/invoice')

# --------- MAKE DISTRIBUTION ---------------
api.add_resource(Make_distribution, "/make/distribution")

# ----------- DELETE ROUTES ---------------------
api.add_resource(Delete_batch, "/delete/batch/<string:batch_no>")
api.add_resource(Delete_invoice, "/delete/invoice/<string:invoice_no>")
