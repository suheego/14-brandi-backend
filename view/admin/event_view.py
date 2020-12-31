import json

from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail, DateMissingOne, SearchTwoInput, FilterDoesNotMatch, SearchFilterRequired

from utils.rules import NumberRule, EventStatusRule, EventExposureRule, DateRule, ProductMenuRule, CategoryFilterRule, \
    PageRule
from flask_request_validator import (
    Param,
    PATH,
    JSON,
    GET,
    validate_params
)


class EventView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('name', GET, str, required=False),
        Param('number', GET, str, required=False, rules=[NumberRule()]),
        Param('status', GET, str, required=False, rules=[EventStatusRule()]),
        Param('exposure', GET, int, required=False, rules=[EventExposureRule()]),
        Param('page', GET, int, required=True, rules=[PageRule()]),
        Param('length', GET, int, required=True),
        Param('start_date', JSON, str, required=False, rules=[DateRule()]),
        Param('end_date', JSON, str, required=False, rules=[DateRule()])
    )
    def get(self, *args):
        data = {
            'name': args[0],
            'number': args[1],
            'status': args[2],
            'exposure': args[3],
            'page': args[4],
            'length': args[5],
            'start_date': args[6],
            'end_date': args[7]
        }
        if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
            raise DateMissingOne('start_date or end_date is missing')

        if data['name'] and data['number']:
            raise SearchTwoInput('search value accept only one of name or number')

        try:
            connection = get_connection(self.database)
            events = self.service.get_events_service(connection, data)
            return jsonify({'message': 'success', 'result': events})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class EventDetailView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('event_id', PATH, int, required=True)
    )
    def get(self, *args):
        data = {
            'event_id': args[0]
        }

        try:
            connection = get_connection(self.database)
            result = self.service.get_event_detail_service(connection, data)
            return jsonify(result)

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class EventProductsCategoryView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('filter', JSON, str, required=True, rules=[CategoryFilterRule()]),
        Param('menu_id', JSON, int, required=False, rules=[ProductMenuRule()]),
        Param('first_category_id', JSON, int, required=False)
    )
    def get(self, *args):
        data = {
            'filter': args[0],
            'menu_id': args[1],
            'first_category_id': args[2]
        }
        if data['filter'] is "none" and (data['menu_id'] or data['first_category_id']):
            raise FilterDoesNotMatch('error: filter does not match')
        elif data['filter'] == "menu":
            if not data['menu_id']:
                raise FilterDoesNotMatch('error: filter does not match')
            if data['first_category_id']:
                raise FilterDoesNotMatch('error: filter does not match')
        elif data['filter'] == "both":
            if not data['menu_id'] or not data['first_category_id']:
                raise FilterDoesNotMatch('error: filter does not match')

        try:
            connection = get_connection(self.database)
            result = self.service.get_products_category_service(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class EventProductsToAddView(MethodView):
    """ 추가할 상품 조회

    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('product_name', GET, str, required=False),
        Param('product_number', GET, str, required=False, rules=[NumberRule()]),
        Param('seller_name', GET, str, required=False),
        Param('seller_number', GET, str, required=False, rules=[NumberRule()]),
        Param('menu_id', JSON, int, required=False, rules=[ProductMenuRule()]),
        Param('main_category_id', JSON, int, required=False),
        Param('sub_category_id', JSON, int, required=False),
        Param('page', GET, int, required=True, rules=[PageRule()]),
        Param('length', GET, int, required=True),
        Param('start_date', JSON, str, required=False, rules=[DateRule()]),
        Param('end_date', JSON, str, required=False, rules=[DateRule()])
    )
    def get(self, *args):
        data = {
            'product_name': args[0],
            'product_number': args[1],
            'seller_name': args[2],
            'seller_number': args[3],
            'menu_id': args[4],
            'main_category_id': args[5],
            'sub_category_id': args[6],
            'page': args[7],
            'length': args[8],
            'start_date': args[9],
            'end_date': args[10]
        }
        if not data['product_name'] \
                and not data['product_number'] \
                and not data['seller_number'] \
                and not data['seller_name'] \
                and not data['menu_id'] \
                and not (data['start_date'] and data['end_date']):
            raise SearchFilterRequired('search filter must be at least one')

        if (data['product_number'] and data['product_name']) or (data['seller_number'] and data['seller_name']):
            raise SearchTwoInput('search value accept only one of name or number')

        if not data['menu_id'] and (data['main_category_id'] or data['sub_category_id']):
            raise FilterDoesNotMatch('upper category is required')

        if not data['main_category_id'] and data['sub_category_id']:
            raise FilterDoesNotMatch('upper category is required')

        if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
            raise DateMissingOne('start_date or end_date is missing')

        try:
            connection = get_connection(self.database)
            products = self.service.get_products_to_post_service(connection, data)
            return jsonify({'message': 'success', 'result': products})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
