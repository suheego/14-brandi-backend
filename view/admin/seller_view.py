from flask import jsonify
from flask.views import MethodView
from utils.rules import NumberRule, DefaultRule
from utils.custom_exceptions import DatabaseCloseFail
from utils.connection import get_connection
from flask_request_validator import (
    Param,
    PATH,
    JSON,
    validate_params
)


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

    def __init__(self, service, database):
        self.service = service
        self.database = database

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

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


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

