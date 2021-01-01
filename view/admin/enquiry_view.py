import json
from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail, DateMissingOne, EventSearchTwoInput

from utils.rules import NumberRule, EventStatusRule, EventExposureRule, DateRule
from flask_request_validator import (
    Param,
    JSON,
    GET,
    validate_params
)

def date_converter(o):
    import datetime
    if isinstance(o, datetime.datetime):
        return o.__str__()

class EnquiryView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('product_name', JSON, str, required=False),
        Param('id', JSON, str, required=False),
        Param('seller_name', JSON, str, required=False),
        Param('membership_number', JSON, str, required=False),
        Param('is_answered', JSON, str, required=False),
        Param('type', JSON, str, required=False),
        Param('start_date', JSON, str, required=False),
        Param('end_date', JSON, str, required=False),
        Param('page', JSON, int, required=True),
        Param('length', JSON, int, required=True),
        Param('response_date', JSON, int, required=False)
    )
    def get(self, *args):
        data = {
            'product_name': args[0],
            'id': args[1],
            'seller_name': args[2],
            'membership_number': args[3],
            'is_answered': args[4],
            'type': args[5],
            'start_date': args[6],
            'end_date': args[7],
            'page': args[8],
            'length': args[9],
            'response_date': args[10]
        }
        if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
            raise DateMissingOne('start_date or end_date is missing')

        if data['product_name'] and data['seller_name']:
            raise EventSearchTwoInput('search value accept only one of name or number')

        try:
            connection = get_connection(self.database)
            enquiries = self.service.get_enquiry_service(connection, data)
            return jsonify({'message': 'success', 'result': enquiries})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
