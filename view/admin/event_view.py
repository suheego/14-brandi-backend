from flask import jsonify
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail


# from utils.rules import NumberRule, GenderRule, AlphabeticRule
# from flask_request_validator import (
#     Param,
#     JSON,
#     validate_params
# )

class EventView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    def get(self, *args):
        try:
            connection = get_connection(self.database)
            events = self.service.get_events_service(connection)
            return jsonify({'message': 'success', 'result': events})

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
