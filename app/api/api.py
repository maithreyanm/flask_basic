'''here the api file is written.. it can also be used for swagger the same api'''
from flask import Blueprint

from library.api_tools import APIEndpoint
from library.api_tools import APIClass

api_blueprint = Blueprint('int_api_bp', __name__, url_prefix='/api/v1')
api_endpoint = APIEndpoint(api_blueprint)


class APIFlask(APIClass):
    @staticmethod
    @api_blueprint.route('/home')
    @api_endpoint.on_call()
    def home():
        return 'WELCOME TO FLASK APP & API'
