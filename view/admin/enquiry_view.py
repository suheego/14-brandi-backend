from flask import jsonify
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule
from flask_request_validator import (
    Param,
    JSON,
    validate_params
)


class EnquiryView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('product_name', JSON, str),
        Param('id', JSON, str),
        Param('seller_name', JSON, str),
        Param('membership_number', JSON, str),
        Param('is_answered', JSON, str),
        Param('type', JSON, str),
        Param('start_date', JSON, str),
        Param('end_date', JSON, str),
        Param('page', JSON, int),
        Param('length', JSON, int),
        Param('response_date', JSON, int)
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

        try:
            connection = get_connection(self.database)
            results = self.service.get_enquiry_service(connection, data)
            return jsonify({'message': 'success', 'result': results})

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
