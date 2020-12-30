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

class SellerSignupView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str),
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
            'seller_attribute_type_id': args[2],
            'name': args[3],
            'english_name': args[4],
            'contact_phone': args[5],
            'service_center_number': args[6],
        }

        try:
            connection = get_connection(self.database)
            self.service.seller_signup_service(connection,data)
            connection.commit()
            return jsonify({'message': 'success'}),200

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

class SellerSigninView(MethodView):

    def __init__(self, service, databses):
        self.service = service
        self.database = databses

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str)
    )

    def post(self, *args):
        data = {
            'username': args[0],
            'password': args[1]
        }

        try:
            connection = get_connection(self.database)
            token = self.service.seller_signin_service(connection, data)
            connection.commit()
            return jsonify({'message':'login success','token': token}),200

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')



