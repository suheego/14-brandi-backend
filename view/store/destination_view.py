from flask.globals import g
from utils.rules import NumberRule, PhoneRule, PostalCodeRule, IsDeleteRule
from utils.custom_exceptions import DatabaseCloseFail
from utils.connection import get_connection
from flask.views import MethodView
from flask_request_validator import(
        Param,
        JSON,
        validate_params
)

from utils.decorator import signin_decorator


class DestinationDetailView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    def get(self, destination_id):
        """GET 메소드: 배송지 상세정보 조회

        pass converter 로 받은 destination_id 에 해당하는
        배송지 상세정보를 조회, 반환해준다.

        Args:
            destination_id : url pass_parameter 로 입력받은 값

        Author: 김기용

        Returns: 201, {"message": "success", "result": {"address1": "주소1",
                                                        "address2": "주소2",
                                                        "default_location": 0,
                                                        "id": 3,
                                                        "phone": "01012345678",
                                                        "post_number": "12345678",
                                                        "recipient": "수취인",
                                                        "user_id": 152
                                                        }}

        Raises:
            500, {'message': 'internal server error', 'errorMessage': format(e)})

        History:
            2020-12-29(김기용): 초기 생성
        """

        connection = None

        try:
            data = dict()
            data['destination_id'] = destination_id

            connection = get_connection(self.database)
            destination_detail = self.service.get_destination_detail_service(connection, data)
            return {'message': 'success', 'result': destination_detail[0]}

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에서 알 수 없는 에러가 발생했습니다.')


class DestinationView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator(False)
    def get(self):
        """GET 메소드:   해당 유저에 대한 배송지 정보 받아오기

        유저에 관련된 모든 배송지 정보를 조회 및 반환한다.

        Args:
            g.account_id: 데코레이터에서 넘겨받은 유저 정보

        Author: 김기용

        Returns: 200, {'message': 'success', 'result': 유저 배송지 정보들}: 배송지 조회 성공

        Raises:
            400, {'message': 'key error', 'errorMessage': '키 값이 일치하지 않습니다.'}
            500, {'message': 'unable to close database', 'errorMessage': '커넥션 종료 실패'}:
            500, {'message': 'internal server error', 'errorMessage': format(e)})

        History:
            2020-12-29(김기용): 초기 생성
            2021-01-02(김기용): 데코레이터 수정
        """

        connection = None

        try:
            data = dict()
            if 'account_id' in g:
                data['account_id'] = g.account_id
            if 'permission_type_id' in g:
                data['permission_type_id'] = g.permission_type_id
            connection = get_connection(self.database)
            destination_detail = self.service.get_destination_detail_by_user_service(connection, data)
            return {'message': 'success', 'result': destination_detail}

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에서 알 수 없는 에러가 발생했습니다.')

    @signin_decorator(True)
    @validate_params(
        Param('recipient', JSON, str),
        Param('phone', JSON, str, rules=[PhoneRule()]),
        Param('address1', JSON, str),
        Param('address2', JSON, str),
        Param('post_number', JSON, str, rules=[PostalCodeRule()]),
    )
    def post(self, *args):
        """POST 메소드:  배송지 추가

        사용자가 입력한 배송지 정보를 받아 데이터베이스에 추가한다.
        최대 배송지 생성 개수는 5개이다.

        Args:
            args =('recipient',
                   'phone',
                   'address1',
                   'address2',
                   'post_number',
                   'default_location',
                   'is_deleted')

        Author: 김기용

        Returns: 201, {'message': 'success'}: 배송지 생성 성공

        Raises:
            400, {'message': 'invalid_parameter', 'error_message': '[데이터]가(이) 유효하지 않습니다.'}
            500, {'message': 'unable_to_close_database', 'errorMessage': '커넥션 종료 실패'}
            500, {'message': 'internal_server_error', 'errorMessage': format(e)})

        History:
            2020-12-28(김기용): 초기 생성
            2020-12-29(김기용): 데코레이터 추가
            2020-12-30(김기용): 수정된 데코레이터반영: 데코레이터에서 permission_type 을 받음
            2021-01-02(김기용): 수정된 데코레이터 반영: signin_decorator(True)
        """
        connection = None

        try:
            data = {
                'user_id': g.account_id,
                'permission_type_id': g.permission_type_id,
                'recipient': args[0],
                'phone': args[1],
                'address1': args[2],
                'address2': args[3],
                'post_number': args[4],
            }

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
                raise DatabaseCloseFail('서버에서 알 수 없는 에러가 발생했습니다.')

    @signin_decorator(True)
    @validate_params(
        Param('destination_id', JSON, str, rules=[NumberRule()]),
        Param('recipient', JSON, str),
        Param('phone', JSON, str, rules=[PhoneRule()]),
        Param('address1', JSON, str),
        Param('address2', JSON, str),
        Param('post_number', JSON, str, rules=[PostalCodeRule()]),
        Param('default_location', JSON, str, rules=[IsDeleteRule()])
    )
    def patch(self, *args):
        """ PATCH 메소드: 배송지 정보 수정

            사용자가 입력한 배송지 정보를 받아 수정한다.
            
            Args: destination_id

            Author: 김기용

            Returns: {'message':'success'}

            Raises: 
                500, {'message': 'unable to close database', 'errorMessage': '커넥션 종료 실패'}
                500, {'message': 'internal server error', 'errorMessage': format(e)})
        """
        connection = None

        try:
            data = dict()
            data['destination_id'] = args[0]
            data['recipient'] = args[1]
            data['phone'] = args[2]
            data['address1'] = args[3]
            data['address2'] = args[4]
            data['post_number'] = args[5]
            data['default_location'] = args[6]
            data['account_id'] = g.account_id
            data['permission_type_id'] = g.permission_type_id

            connection = get_connection(self.database)
            self.service.update_destination_info_service(connection, data)
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
                raise DatabaseCloseFail('서버에서 알 수 없는 에러가 발생했습니다')

    @signin_decorator(True)
    @validate_params(
        Param('destination_id', JSON, str, rules=[NumberRule()])
    )
    def delete(self, *args):
        """DELETE 메소드:  배송지 삭제

        Args:
            args =('user_id')

        Author: 김기용

        Returns: 200, {'message': 'success'}: 배송지 삭제 성공

        Raises:
            500, {'message': 'unable_to_close_database', 'errorMessage': '커넥션 종료 실패'}
            500, {'message': 'internal_server_error', 'errorMessage': format(e)}): 서버 에러

        History:
            2020-12-29(김기용): 초기 생성
            2020-12-30(김기용): 데코레이터 추가
        """

        connection = None
        
        try:
            data = dict()
            data['destination_id'] = args[0]
            data['account_id'] = g.account_id
            data['permission_type_id'] = g.permission_type_id

            connection = get_connection(self.database)
            self.service.delete_destination_service(connection, data)
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
                raise DatabaseCloseFail('서버에서 알 수 없는 에러가 발생했습니다')
