
from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, GenderRule, AlphabeticRule, DefaultRule
from flask_request_validator import (
    Param,
    PATH,
    JSON,
    validate_params
)


class SellerSignupView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str),
        Param('seller_attribute_type_id', JSON, str),
        Param('name', JSON, str),
        Param('english_name', JSON, str),
        Param('contact_phone', JSON, str),
        Param('service_center_number', JSON, str),
    )
    def post(self, *args):

        data = {
            'username' : args[0],
            'password' : args[1],
            'seller_attribute_type_id': args[2],
            'name': args[3],
            'english_name': args[4],
            'contact_phone': args[5],
            'service_center_number': args[6],
        }

        try:
            connection = get_connection(self.database)
            self.service.seller_signup_service(connection,data)
            connection.commit()
            return jsonify({'message': 'success'}),200


        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

                
class SellerSigninView(MethodView):

    def __init__(self, service, databses):
        self.service = service
        self.database = databses

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str)
    )

    def post(self, *args):
        data = {
            'username': args[0],
            'password': args[1]
        }

        try:
            connection = get_connection(self.database)
            token = self.service.seller_signin_service(connection, data)
            connection.commit()
            return jsonify({'message':'login success','token': token}),200

        except Exception as e:
            connection.rollback()                

            
class SellerInfoView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service : SellerInfoService 클래스

    Author:
        이영주

    History:
        2020-12-28(이영주): 초기 생성
    """
    @validate_params(
      Param('account_id', PATH, str, required=True, rules=[NumberRule()])
    )
    def get(self, *args):
        """GET 메소드: 
            해당 셀러의 정보를 조회.
            account_id 에 해당되는 셀러를 테이블에서 조회 후 가져온다.

        Args: 
            account_id

        Author: 
            이영주
        
        Returns:
            result seller
            
        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'seller does not exist error', 'errorMessage': 'seller_does_not_exist'}: 셀러 정보 조회 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-28(이영주): 초기 생성
        """
        data = {
            'account_id': args[0]
        }
        try:
            connection = get_connection(self.database)
            seller = self.service.get_seller_info(connection, data)
            return jsonify({'message' : 'success', 'result' : seller}), 200

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('account_id', JSON, str, required=True, rules=[NumberRule()]),
        Param('seller_discription', JSON, str, required=False, rules=[DefaultRule()]),
        Param('seller_title', JSON, str, required=False, rules=[DefaultRule()]),
        Param('status_id', PATH, str, required=False, rules=[NumberRule()])
    )
    def patch(self, *args):
        """PATCH 메소드: 
                셀러 정보 수정

        Args: 

        Author: 
            이영주 

        Returns:
            200, {'message': 'success'}                                                             : 셀러 정보변경   

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'unable to update', 'errorMessage': 'unable_to_update'}                : 셀러 정보 수정 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-29(이영주): 초기 생성
        """
        data = {
            'account_id': args[0],
            'seller_discription': args[1],
            'seller_title': args[2],
            'status_id': args[3],
        }
        try:
            connection = get_connection(self.database)
            self.service.patch_seller_info(connection, data)
            connection.commit()
            return jsonify({'message': 'success'}), 200


class SellerHistoryView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('account_id', PATH, str, required=False, rules=[NumberRule()])
    )
    def get(self, *args):
        """GET 메소드: 해당 셀러의 히스토리 정보를 조회.

        account_id 에 해당되는 셀러 히스토리를 테이블에서 조회 후 가져온다.

        Args:
            args = (account_id)

        Author:
            이영주

        Returns:
            seller_history

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'seller does not exist error', 'errorMessage': 'seller_does_not_exist'}: 셀러 정보 조회 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-28(이영주): 초기 생성
        """
        data = {
            'account_id' : args[0]
        }
        try:
            connection = get_connection(self.database)
            seller_history = self.service.get_seller_history(connection, data)
            return jsonify({'message' : 'success', 'result' : seller_history}), 200

        except exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')