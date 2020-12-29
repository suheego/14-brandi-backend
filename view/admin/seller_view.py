from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, GenderRule, AlphabeticRule
from flask_request_validator import (
    Param,
    JSON,
    validate_params
)

class SellerView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str),
        Param('permission_type_id', JSON, int),
        Param('seller_attribute_type_id', JSON, str),
        Param('name', JSON, str),
        Param('english_name', JSON, str),
        Param('contact_phone', JSON, str),
        Param('service_center_number', JSON, str),
    )
    def post(self, *args):

        data = {
            'username' : args[0],
            'password' : args[1],
            'permission_type_id' : args[2],
            'seller_attribute_type_id': args[3],
            'name': args[4],
            'english_name': args[5],
            'contact_phone': args[6],
            'service_center_number': args[7],
        }
        try:
            connection = get_connection(self.database)
        #     self.service.post_account_insert_service(connection, data)
        #     self.service.post_seller_insert_service(connection, data)
        #     self.service.post_seller_history_insert_service(connection, data)
            self.service.check_account_service(connection,data)
        #    self.service.post_seller_insert_service(connection, data)
            connection.commit()
            return {'message': 'success'}


        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')



