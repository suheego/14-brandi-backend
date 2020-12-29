from flask import jsonify
from flask.views import MethodView
from utils.rules import NumberRule
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

    Author: 이영주

    History:
        2020-12-28(이영주): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('account_id', PATH, str, required=False, rules=[NumberRule()])
    )
    def get(self, *args):
        data = {
            'account_id': args[0]
        }
        """GET 메소드: 해당 셀러의 정보를 조회.

        account_id 에 해당되는 셀러를 테이블에서 조회 후 가져온다.

        Args: args = (account_id)

        Author: 이영주
        
        Returns:
        {
            "message": "success",
            "result": [
                {
                    "account_id": 50,
                    "background_image_url": "https://img.freepik.com/free-psd/top-view-t-shirt-concept-mock-up_23-2148809114.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477",
                    "profile_image_url": "https://img.freepik.com/free-psd/logo-mockup-white-paper_1816-82.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477",
                    "seller_attribute_type_id": 2,
                    "seller_english_name": "i am seller_50",
                    "seller_name": "나는셀러50",
                    "seller_status_type_id": 3,
                    "username": "seller49"
                }
            ]
        }

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'seller does not exist error', 'errorMessage': 'seller_does_not_exist'}: 셀러 정보 조회 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-28(이영주): 초기 생성
            2020-12-29(이영주): 작업중
        """
        try:
            connection = get_connection(self.database)
            seller = self.service.get_seller_info_service(connection, data)
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
        Param('seller_discription', JSON, str, required=False, rules=[NumberRule()]),
    )
    def patch(self, args):
        print(args)
        """PATCH 메소드: 셀러 정보 수정

        Args: 

        Author: 이영주 

        Returns:
            200, {'message': 'success'}                                                             : 셀러 정보변경   

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'unable to update', 'errorMessage': 'unable_to_update'}                : 셀러 정보 수정 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-29(이영주): 초기 생성/ 작업중 
        """

        data = {
            'seller_discription': args[0]
        }
        try:
            connection = get_connection(self.database)
            seller = self.service.patch_seller_info_service(connection, data)
            return jsonify({'message' : 'success', 'result' : seller}), 200

        except Exception as e:
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
    def get(self,*args):
        """GET 메소드: 해당 셀러의 히스토리 정보를 조회.

        account_id 에 해당되는 셀러 히스토리를 테이블에서 조회 후 가져온다.

        Args: args = (account_id)

        Author: 이영주

        Returns:
        {
            "message": "success",
            "result": [
                {
                    "id": 50,
                    "seller_status": "휴점",
                    "updated_at": "Thu, 24 Dec 2020 23:31:43 GMT",
                    "updater_name": "seller50"
                }
            ]
        }

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
            seller_history = self.service.get_seller_history_service(connection, data)
            print()
            return jsonify({'message' : 'success', 'result' : seller_history}), 200

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')