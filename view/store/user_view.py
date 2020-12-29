from flask.views import MethodView
from flask import jsonify

from flask_request_validator import (
    validate_params,
    Param,
    JSON
)

from google.oauth2 import id_token
from google.auth.transport import requests

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import PasswordRule, PhoneRule, EmailRule, UsernameRule


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
        Param('username', JSON, str, rules=[UsernameRule()]),
        Param('password', JSON, str, rules=[PasswordRule()]),
        Param('phone', JSON, str, rules=[PhoneRule()]),
        Param('email', JSON, str, rules=[EmailRule()])
    )
    def post(self, *args):
        """POST 메소드: 유저생성

            Args: args = ('username', 'password', 'phone', 'email')

            Author: 김민구

            Returns:
                200, {'message': 'success'}                                                               : 유저 생성 성공

            Raises:
                400, {'message': 'invalid_parameter', 'errorMessage': str(e)}                        : 잘못된 요청값
                400, {'message': 'key_error', 'errorMessage': 'key_error_' + format(e)}              : 잘못 입력된 키값
                403, {'message': 'user_already_exist', errorMessage': 'already_exist' + _중복 데이터}   : 중복 유저 생성 실패
                500, {'message': 'user_create_denied', 'errorMessage': 'account_create_fail'}        : 유저 생성 실패
                500, {'message': 'user_create_denied', 'errorMessage': 'user_create_fail'}           : 유저 생성 실패
                500, {'message': 'database_connection_fail', 'errorMessage': 'database_close_fail'}  : 커넥션 종료 실패
                500, {'message': 'database_error', 'errorMessage': 'database_error_' + format(e)}    : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'errorMessage': format(e)})                : 서버 에러

            History:
                2020-20-28(김민구): 초기 생성
        """

        try:
            data = {
                'username': args[0],
                'password': args[1],
                'phone': args[2],
                'email': args[3]
            }

            connection = get_connection(self.database)
            self.service.sign_up_service(data, connection)
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
                raise DatabaseCloseFail('database_close_fail')


class SignInView(MethodView):
    """ Presentation Layer

        Attributes:
            service : UserService 클래스
            database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-20-29(김민구): 초기 생성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str)
    )
    def post(self, *args):
        """ POST 메소드: 유저 로그인

            Args: args = ('username', 'password')

            Author: 김민구

            Returns:
                200, {'message': 'success', 'token': access_token}                                   : 유저 생성 성공

            Raises:
                400, {'message': 'invalid_parameter', 'errorMessage': str(e)}                        : 잘못된 요청값
                400, {'message': 'key_error', 'errorMessage': 'key_error_' + format(e)}              : 잘못 입력된 키값
                403, {'message': 'invalid_user', 'errorMessage': 'invalid_user'}                     : 로그인 실패s
                500, {'message': 'database_connection_fail', 'errorMessage': 'database_close_fail'}  : 커넥션 종료 실패
                500, {'message': 'database_error', 'errorMessage': 'database_error_' + format(e)}    : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'errorMessage': format(e)})                : 서버 에러

            History:
                2020-20-29(김민구): 초기 생성
        """

        try:
            data = {
                'username': args[0],
                'password': args[1]
            }
            connection = get_connection(self.database)
            access_token = self.service.sign_in_service(data, connection)
            return jsonify({'message': 'success', 'token': access_token}), 200

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database_close_fail')
