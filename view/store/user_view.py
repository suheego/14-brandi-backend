from flask.views import MethodView
from flask import jsonify

from flask_request_validator import (
    validate_params,
    Param,
    JSON
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail


class SignUpView(MethodView):
    """ Presentation Layer

    Attributes:
        service : UserService 클래스
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

    Author: 김민구

    History:
        2020-20-28(김민구): 초기 생성 / bcrypt 까지 완료.
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str),
        Param('phone', JSON, str),
        Param('email', JSON, str)
    )
    def post(self, *args):
        try:
            data = {
                'username': args[0],
                'password': args[1],
                'phone': args[2],
                'email': args[3]
            }
            connection = get_connection(self.database)
            self.service.signup_service(data, connection)
            connection.commit()
            return jsonify({'message': 'success'}), 200

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
