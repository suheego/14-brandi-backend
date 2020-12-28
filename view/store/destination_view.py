from utils.rules import NumberRule, PhoneRule, PostalCodeRule, IsDeleteRule
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

    def get(self):
        pass

    @validate_params(
        Param('user_id', JSON, str, rules=[NumberRule()]),
        Param('recipient', JSON, str),
        Param('phone', JSON, str, rules=[PhoneRule()]),
        Param('address1', JSON, str),
        Param('address2', JSON, str),
        Param('post_number', JSON, str, rules=[PostalCodeRule()]),
        Param('default_location', JSON, str),
        Param('is_deleted', JSON, str, rules=[IsDeleteRule()])
    )
    def post(self,*args):
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

        """POST 메소드:  유저생성

        Args:
            args =('user_id',
                   'recipient',
                   'phone',
                   'address1',
                   'address2',
                   'post_number',
                   'default_location',
                   'is_deleted')

        Author: 김기용

        Returns: 201, {'message': 'success'}: 배송지 생성 성공

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                                        : 잘못 입력된 키값
            400, {'message': 'destination_creatation_denied', 'errorMessage': 'destination_creatation_denied'}: 배송지 생성 실패
            400, {'message': 'not_a_user', 'errorMessage': 'not_a_user'}                                      : 유저 불일치 
            401, {'message': 'account_does_not_exist', 'errorMessage': 'account_does_not_exist}               : 계정 정보 없음
            500, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}          : 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                             : 서버 에러

        History:
            2020-12-28(김기용): 초기 생성
        """

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

    def patch(self):
        pass

    def delete(self):
        pass


