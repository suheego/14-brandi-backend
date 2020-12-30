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

class EventView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('name', GET, str, required=False),
        Param('number', GET, str, required=False, rules=[NumberRule()]),
        Param('status', GET, str, required=False, rules=[EventStatusRule()]),
        Param('exposure', GET, int, required=False, rules=[EventExposureRule()]),
        Param('page', GET, int, required=True),
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
            raise EventSearchTwoInput('search value accept only one of name or number')

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
