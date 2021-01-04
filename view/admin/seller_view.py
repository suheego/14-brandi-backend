from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, GenderRule, AlphabeticRule
from flask_request_validator import (
    Param,
    JSON,
    FORM,
    GET,
    validate_params
)

class SellerSearchView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('page', GET, int, required=False),
        Param('page_view', GET, int, required=False),
        Param('account_id', JSON, int, required=False),
        Param('username', JSON, str, required=False),
        Param('seller_english_name', JSON, str, required=False),
        Param('seller_name', JSON, str, required=False),
        Param('contact_name', JSON, str, required=False),
        Param('contact_phone', JSON, str, required=False),
        Param('contact_email', JSON, str, required=False),
        Param('seller_attribute_type_name', JSON, str, required=False),
        Param('seller_status_type_name', JSON, str, required=False),
        Param('updated_at', JSON, str, required=False),
        Param('start_date',JSON, str, required=False),
        Param('end_date', JSON, str, required=False)
    )

    def get(self, *args):
        try:
            data = {
                'account_id' : args[2],
                'username' : args[3],
                'seller_english_name' : args[4],
                'seller_name': args[5],
                'contact_name': args[6],
                'contact_phone': args[7],
                'contact_email': args[8],
                'seller_attribute_type_name': args[9],
                'seller_status_type_name': args[10],
                'updated_at': args[11],
                'start_date': args[12],
                'end_date' : args[13]
            }

            page = request.args.get('page',1)
            page_view = request.args.get('page_view',10)

            connection = get_connection(self.database)
            seller_list = self.service.seller_search_service(connection, data, page, page_view)
            return jsonify({'message':'success', 'result': seller_list}),200

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail in seller_list_view')

class SellerSignupView(MethodView):

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



