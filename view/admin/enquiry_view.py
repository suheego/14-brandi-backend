import json

from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail, DateMissingOne, EventSearchTwoInput

from utils.rules import NumberRule, EventStatusRule, DateRule, PageRule
from flask_request_validator import (
    Param,
    PATH,
    JSON,
    GET,
    validate_params
)


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
        Param('page', JSON, int, required=True, rules=[PageRule()]),
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


class AnswerView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('enquiry_id', PATH, int, required=True)
    )
    def get(self, *args):
        data = {
            'enquiry_id': args[0]
        }

        try:
            connection = get_connection(self.database)
            result = self.service.get_answer_service(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('enquiry_id', PATH, int),
        Param('answer', JSON, str)
    )
    def post(self, *args):
        data = {
            'enquiry_id': args[0],
            'answer': args[1]
        }
        try:
            connection = get_connection(self.database)
            self.service.post_answer_service(connection, data)
            connection.commit()
            return {'message': 'success'}
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('enquiry_id', PATH, int),
        Param('answer', JSON, str)
    )
    def put(self, *args):
        data = {
            'enquiry_id': args[0],
            'answer': args[1]
        }

        try:
            connection = get_connection(self.database)
            self.service.put_answer_service(connection, data)
            connection.commit()
            return {'message': 'success'}
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('enquiry_id', PATH, int),
    )
    def delete(self, *args):
        data = {
            'enquiry_id': args[0]
        }

        try:
            connection = get_connection(self.database)
            self.service.delete_answer_service(connection, data)
            connection.commit()
            return {'message': 'success'}
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
