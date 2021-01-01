from flask.views import MethodView
from flask import jsonify

from flask_request_validator import (
    validate_params,
    Param,
    GET,
    PATH
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import PositiveInteger


class EventBannerListView(MethodView):
    """

    """

    def __init__(self, services, database):
        self.event_list_service = services.event_list_service
        self.database = database

    @validate_params(
        Param('offset', GET, int),
        Param('limit', GET, int),
        Param('is_proceeding', GET, bool)
    )
    def get(self, *args):
        """

        Args:
            *args:

        Returns:

        """

        connection = None
        try:
            data = {
                'offset': args[0],
                'limit': args[1],
                'is_proceeding': args[2]
            }
            connection = get_connection(self.database)
            result = self.event_list_service.event_banner_list_logic(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class EventDetailInformationView(MethodView):
    """

    """

    def __init__(self, services, database):
        self.event_list_service = services.event_list_service
        self.database = database

    @validate_params(
        Param('event_id', PATH, int, rules=[PositiveInteger()])
    )
    def get(self, *args):
        """

        Args:
            *args:

        Returns:

        """

        connection = None
        try:
            event_id = args[0]
            connection = get_connection(self.database)
            result = self.event_list_service.event_detail_information_logic(connection, event_id)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class EventDetailButtonListView(MethodView):
    """

    """

    def __init__(self, services, database):
        self.event_list_service = services.event_list_service
        self.database = database

    @validate_params(
        Param('event_id', PATH, int, rules=[PositiveInteger()])
    )
    def get(self, *args):
        """

        Args:
            *args:

        Returns:

        """

        connection = None
        try:
            event_id = args[0]
            connection = get_connection(self.database)
            result = self.event_list_service.event_detail_button_list_logic(connection, event_id)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class EventDetailListView(MethodView):
    """

    """

    def __init__(self, services, database):
        self.event_list_service = services.event_list_service
        self.database = database

    @validate_params(
        Param('offset', GET, int),
        Param('limit', GET, int),
        Param('event_id', PATH, int, rules=[PositiveInteger()])
    )
    def get(self, *args):
        """

        Args:
            *args:

        Returns:

        """

        connection = None
        try:
            data = {
                'offset': args[0],
                'limit': args[1],
                'event_id': args[2]
            }
            connection = get_connection(self.database)
            result = self.event_list_service.event_detail_list_logic(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')