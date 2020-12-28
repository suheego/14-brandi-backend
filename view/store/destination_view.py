from utils.rules import NumberRule
from utils.custom_exceptions import DatabaseCloseFail
from flask.json import jsonify
from utils.connection import get_connection
from flask.views import MethodView
from flask_request_validator import(
        Param,
        JSON,
        validate_params
)


class DestinationSelectView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    def get(self, destinations_id):
        data = {
                'destination_id': destinations_id
        }

        try:
            connection = get_connection(self.database)
            destination = self.service.destination_select_service(connection, data)
            return jsonify({'message': 'success', 'result':destination})

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class DestinationView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('user_id', JSON, str, rules=[NumberRule()]),
        Param('recipient', JSON, str),
        Param('phone', JSON, str),
        Param('address1', JSON, str),
        Param('address2', JSON, str),
        Param('post_number', JSON, str),
        Param('default_location', JSON, str),
        Param('is_deleted', JSON, str)
    )
    def get(self, *args):
        data = {
            'user_id': args[0],
            'recipient': args[1],
            'phone': args[2],
            'address1': args[3],
            'address2': args[4],
            'post_number': args[5],
            'default_location': args[6],
            'is_deleted': args[7]
        }

        try:
            connection = get_connection(self.database)
            self.service.create_destination_service(connection, data)
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


    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


