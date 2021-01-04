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

    def __init__(self, service , database):
        self.service = service
        self.database = database

    def get(self, destination_id):
        """GET 메소드: 배송지 상세정보 조회

        Args:
            destination_id : url pass_parameter 로 입력받은 값

        Author: 김기용

        Returns: 201, {'message': 'success', 'reuslt':'배송지 상세 정보'}: 배송지 생성 성공

        Raises:
            400, {'message': 'key_error', 'errorMessage': 'key_error'}                            : 잘못 입력된 키값
            400, {'message': 'destination_dose_not_exist', 'errorMessage': '존재하지 않는 배송지'}: 배송지 조회 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                 : 서버 에러

        History:
            2020-12-29(김기용): 초기 생성
        """
        data = dict()
        data['destination_id'] = destination_id

        try:
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

    @signin_decorator(True)
    def get(self):
        """GET 메소드:   해당 유저에 대한 배송지 정보 받아오기

        Args:
            g.account_id: 데코레이터에서 넘겨받은 유저 정보


        Author: 김기용

        Returns: 200, {'message': 'success', 'result': 유저 배송지 정보들}: 배송지 조회 성공

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'not_a_user', 'errorMessage': 'not_a_user'}                            : 유저 불일치 
            401, {'message': 'account_does_not_exist', 'errorMessage': 'account_does_not_exist}     : 계정 정보 없음
            500, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-29(김기용): 초기 생성
            2021-01-02(김기용): 데코레이터 수정
        """

        data = dict()
        data['account_id'] = g.account_id
        data['permission_type_id'] = g.permission_type_id

        try:
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
            400, {'message': 'key error', 'errorMessage': 'key_error'}                                       : 잘못 입력된 키값
            400, {'message': 'destination_creatation_denied', 'errorMessage': '배송지를 생성하지 못했습니다'}: 배송지 생성 실패
            400, {'message': 'not_a_user', 'errorMessage': 'not_a_user'}                                     : 유저 불일치
            400, {'message': 'data_limit_reached', 'errorMessage': 'max_destination_limit_reached'}          : 최대 생성 개수 초과
            401, {'message': 'account_does_not_exist', 'errorMessage': 'account_does_not_exist}              : 계정 정보 없음
            500, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}         : 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                            : 서버 에러

        History:
            2020-12-28(김기용): 초기 생성
            2020-12-29(김기용): 데코레이터 추가
            2020-12-30(김기용): 수정된 데코레이터반영: 데코레이터에서 user_type을 받음
            2021-01-02(김기용): 수정된 데코레이터 반영: signin_decorator(True)
        """

        data = {
            'user_id': g.account_id,
            'permission_type_id': g.permission_type_id,
            'recipient': args[0],
            'phone': args[1],
            'address1': args[2],
            'address2': args[3],
            'post_number': args[4],
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
            
            Args: destination_id

            Author: 김기용

            Returns: {'message':'success'}

            Raises: 
                400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
                400, {'message': 'not_a_user', 'errorMessage': 'not_a_user'}                            : 유저 불일치
                500, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
                500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러
        """
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

        try:
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
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            401, {'message': 'account_does_not_exist', 'errorMessage': 'account_does_not_exist}     : 계정 정보 없음
            500, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-29(김기용): 초기 생성
            2020-12-30(김기용): 데코레이터 추가
        """
        data = dict()
        data['destination_id'] = args[0]
        data['account_id'] = g.account_id
        data['permission_type_id'] = g.permission_type_id
        
        try:
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
