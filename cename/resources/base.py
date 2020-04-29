from flask_restful import Resource, reqparse
from flask import request
from cename.models import Region
from datetime import datetime

class BaseResource(Resource):
    """
    Abstraction of major functionalities and methods for resources.
    """

    def __init__(self):
        self.arg_parser = reqparse.RequestParser()
        self.arguments_list = [] # abstract a list of arguments pasrsing

    def add_argument(self, arg):
        """Add an argument to the parser"""
        self.arg_parser.add_argument(arg['name'], arg['type'], help=arg['help'])

    def init_args(self):
        """Initialize the arguments for parsing"""
        if len(self.arguments_list) == 0:
            return 
        for arg in self.arguments_list:
            self.add_argument(arg)

    @staticmethod
    def get_request_data():
        return request.data
    
    def parse_args(self):
        """Parse the request arguments"""
        return self.arg_parser.parse_args()

    def parse_query(self, query_res):
        parsed_response = []
        if len(query_res) > 0:
            for data in query_res:
                parsed_response.append(data.jsonify())
        return parsed_response
        
    @staticmethod
    def convert_to_date(s):
        return datetime.strptime(s, "%m/%d/%y")

    def fetch_from_db(self, db_model, row_id=None, **kwargs):
        temp = []
        try:
            if row_id == None:
                temp = db_model.query.all()
            else:
                # beacuse of the parse_query method, 
                # the passed arg must always be an iterable (tuple or list)
                temp = [db_model.query.get(row_id)] or []
        except Exception as e: 
            if kwargs.get('err_callback'):
                kwargs.get('err_callback')(e)
        # if no error was encountered 
        # and temp is not empty, then parse the 
        else:
            if len(temp) > 0:
                temp = self.parse_query(temp)
        finally:
            return temp


class Get_regions(BaseResource):
    def __init__(self):
        super().__init__()
        self.arguments_list = []
        self.init_args()
        self.args = self.parse_args()

    def get(self):
        query = Region.query.all()
        return self.parse_query(query), 200