from flask.views import MethodView
from flask import jsonify, request

from flask_request_validator import (
    validate_params,
    Param,
    JSON
)

from google.oauth2 import id_token
from google.auth.transport import requests

from utils.connection import get_connection
from utils.custom_exceptions import InvalidToken, DatabaseCloseFail
from utils.rules import PasswordRule, EmailRule, UsernameRule, PhoneRule


class SignUpView(MethodView):
    """ Presentation Layer

        Attributes:
            user_service  : UserService 클래스
            database      : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-12-28(김민구): 초기 생성 / bcrypt 까지 완료
            2020-12-29(김민구): 각 Param에 rules 추가, 에러 구문 수정
            2020-12-31(김민구): 모든 service를 담고 있는 services 클래스로 유연하게 처리 / 에러 문구 변경
            2021-01-02(김민구): 데이터 조작 에러 추가
    """

    def __init__(self, services, database):
        self.user_service = services.user_service
        self.database = database

    @validate_params(
        Param('username', JSON, str, rules=[UsernameRule()]),
        Param('password', JSON, str, rules=[PasswordRule()]),
        Param('phone', JSON, str, rules=[PhoneRule()]),
        Param('email', JSON, str, rules=[EmailRule()])
    )
    def post(self, *args):
        """POST 메소드: 유저생성

            Args:
                args = ('username', 'password', 'phone', 'email')

            Author: 김민구

            Returns:
                200, {'message': 'success'}                                                         : 유저 생성 성공

            Raises:
                400, {'message': 'invalid_parameter', 'errorMessage': '[데이터]가(이) 유효하지 않습니다.'} : 잘못된 요청값
                400, {'message': 'key_error', 'error_message': format(e)}                          : 잘못 입력된 키값
                403, {'message': 'user_already_exist', 'error_message': '이미 사용중인 [데이터] 입니다.'} : 중복 유저 존재
                500, {
                        'message': 'database_connection_fail',
                        'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                      }                                                                             : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러
                500, {'message': 'data_manipulation_fail', 'error_message': '유저 등록을 실패하였습니다.'}  : 데이터 조작 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})              : 서버 에러

            History:
                2020-12-28(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
                2021-01-02(김민구): 데이터 조작 에러 추가
        """

        connection = None
        try:
            data = {
                'username': args[0],
                'password': args[1],
                'phone': args[2],
                'email': args[3]
            }

            connection = get_connection(self.database)
            self.user_service.sign_up_logic(data, connection)
            connection.commit()
            return jsonify({'message': 'success'}), 200

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class SignInView(MethodView):
    """ Presentation Layer

        Attributes:
            user_service : UserService 클래스
            database     : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-12-29(김민구): 초기 생성
            2020-12-31(김민구): 에러 문구 변경
            2021-01-02(김민구): 데이터 조작 에러 추가
    """

    def __init__(self, services, database):
        self.user_service = services.user_service
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
                200, {'message': 'success', 'token': token}                                         : 유저 로그인 성공

            Raises:
                400, {'message': 'invalid_parameter', 'errorMessage': '[데이터]가(이) 유효하지 않습니다.'}  : 잘못된 요청값
                400, {'message': 'key_error', 'error_message': format(e)}                           : 잘못 입력된 키값
                403, {'message': 'invalid_user', 'error_message': '로그인에 실패했습니다.'}               : 로그인 실패
                500, {'message': 'create_token_denied', 'error_message': '로그인에 실패했습니다.'}        : 토큰 생성 실패
                500, {
                        'message': 'database_connection_fail',
                        'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                      }                                                                             : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})              : 서버 에러

            History:
                2020-12-29(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
                2021-01-02(김민구): 데이터 조작 에러 추가
        """

        connection = None
        try:
            print('asdfasdfasdfsadf')
            print(args)
            data = {
                'username': args[0],
                'password': args[1]
            }
            connection = get_connection(self.database)
            token = self.user_service.sign_in_logic(data, connection)
            print(token)
            return jsonify({'message': 'success', 'token': token}), 200

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class GoogleSocialSignInView(MethodView):
    """ Presentation Layer

        Attributes:
            user_service  : UserService 클래스
            database      : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-12-29(김민구): 초기 생성
            2020-12-31(김민구): 에러 문구 변경
            2021-01-02(김민구): 데이터 조작 에러 추가
    """

    def __init__(self, services, database):
        self.user_service = services.user_service
        self.database = database

    def post(self):
        """ POST 메소드: 유저 구글 소셜 로그인

            Args: None

            Headers:
                Authorization : 구글 토큰

            Author: 김민구

            Returns:
                200, {'message': 'success', 'token': token}                                           : 유저 로그인 성공

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)}                             : 잘못 입력된 키값
                403, {'message': 'invalid_token', 'error_message': '구글 소셜 로그인에 실패하였습니다.'}       : 유효하지 않은 토큰
                403, {'message': 'invalid_user', 'error_message': '구글 소셜 로그인에 실패했습니다.'}         : 유효하지 않은 유저
                500, {
                        'message': 'database_connection_fail',
                        'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                      }                                                                              : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'data_manipulation_fail', 'error_message': '소셜 로그인을 실패하였습니다.'} : 데이터 조작 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러

            History:
                2020-12-29(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
                2021-01-02(김민구): 데이터 조작 에러 추가
        """

        connection = None
        try:
            print('asdfasdfasdfasdf')
            google_token = request.headers.get('Authorization')
            connection = get_connection(self.database)
            user_info = id_token.verify_oauth2_token(google_token, requests.Request())
            token = self.user_service.social_sign_in_logic(connection, user_info)
            connection.commit()
            return jsonify({'message': 'success', 'token': token}), 200

        except Exception as e:
            connection.rollback()
            raise e

        except ValueError:
            connection.rollback()
            raise InvalidToken('구글 소셜 로그인에 실패하였습니다.')

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')
