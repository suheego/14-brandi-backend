from flask.views import MethodView
from flask import jsonify, g

from flask_request_validator import (
    validate_params,
    Param,
    GET,
    PATH
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail, InvalidUser
from utils.decorator import signin_decorator
from utils.rules import EnquiryUserTypeRule, PositiveInteger, EnquiryAnswerTypeRule


class ProductEnquiryListView(MethodView):
    """ Presentation Layer

        Attributes:
            product_enquiry_list_service : ProductEnquiryService 클래스
            database                     : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-01-04(김민구): 초기 생성
    """

    def __init__(self, services, database):
        self.product_enquiry_list_service = services.product_enquiry_list_service
        self.database = database

    @signin_decorator(False)
    @validate_params(
        Param('product_id', PATH, int, rules=[PositiveInteger()]),
        Param('offset', GET, int),
        Param('type', GET, str, rules=[EnquiryUserTypeRule()])
    )
    def get(self, *args):
        """ GET 메소드: 상품 Q&A 리스트 조회

            Args:
                product_id = 0부터 시작
                offset  = 30단위
                type = self 혹은 all

            Author: 김민구

            Returns: Q&A 리스트 조회 성공
                200, {
                        'message': 'success',
                        'result': {
                            "enquiries": [
                                {
                                    "answer": {
                                        "account_id": 2,
                                        "content": "답변드릴게요",
                                        "created_at": "2021-01-04 12:38:12",
                                        "enquiry_id": 102,
                                        "id": 52,
                                        "seller_name": "나는셀러2"
                                    },
                                    "content": "임시질문인데요2(답변감사합니다)",
                                    "created_at": "2021-01-04 11:31:26",
                                    "enquiry_id": 102,
                                    "enquiry_type_id": 1,
                                    "enquiry_type_name": "상품 문의",
                                    "is_completed": 1,
                                    "is_secret": 0,
                                    "product_id": 1,
                                    "user_id": 152
                                }
                            ],
                            "enquiry_types": [
                                {
                                    "id": 1,
                                    "name": "상품 문의"
                                }
                            ]
                        }
                    }

            Raises:
                400, {'message': 'invalid_parameter', 'error_message': '[데이터]가(이) 유효하지 않습니다.'}  : 잘못된 요청값
                400, {'message': 'key_error', 'error_message': format(e)}                            : 잘못 입력된 키값
                500, {
                    'message': 'database_connection_fail',
                    'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                    }                                                                                : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러

            History:
                2020-01-04(김민구): 초기 생성

            Notes:
                로그인 후 type이 self라면 해당 상품에서 해당 유저의 Q&A만 보여주고 all이라면 로그인 유무 상관 없이 해당 상품의 모든 Q&A를 보여준다.
        """

        connection = None
        try:
            data = {
                'product_id': args[0],
                'offset': args[1],
                'type': args[2]
            }

            if data['type'] == 'self':
                if 'account_id' in g:
                    data['user_id'] = g.account_id
                elif 'account_id' not in g:
                    raise InvalidUser('로그인이 필요합니다.')

            connection = get_connection(self.database)
            result = self.product_enquiry_list_service.product_enquiry_list_logic(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class MyPageEnquiryListView(MethodView):
    """ Presentation Layer

        Attributes:
            product_enquiry_list_service : ProductEnquiryService 클래스
            database                     : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-01-04(김민구): 초기 생성
    """

    def __init__(self, services, database):
        self.product_enquiry_list_service = services.product_enquiry_list_service
        self.database = database

    @signin_decorator()
    @validate_params(
        Param('type', GET, str, rules=[EnquiryAnswerTypeRule()]),
        Param('offset', GET, int)
    )
    def get(self, *args):
        """ GET 메소드: 유저의 Q&A 리스트 조회

            Args:
                offset  = 30단위
                type = wait 혹은 complete 혹은 all

            Author: 김민구

            Returns: Q&A 리스트 조회 성공
                200, {
                        'message': 'success',
                        'result': {
                            "enquiries": [
                                {
                                    "answer": {
                                        "account_id": 2,
                                        "content": "답변드릴게요",
                                        "created_at": "2021-01-04 12:38:12",
                                        "enquiry_id": 102,
                                        "id": 52,
                                        "seller_name": "나는셀러2"
                                    },
                                    "content": "임시질문인데요2(답변감사합니다)",
                                    "created_at": "2021-01-04 11:31:26",
                                    "enquiry_id": 102,
                                    "enquiry_type_id": 1,
                                    "enquiry_type_name": "상품 문의",
                                    "is_completed": 1,
                                    "is_secret": 0,
                                    "product_id": 1,
                                    "user_id": 152
                                }
                            ]
                        }
                    }

            Raises:
                400, {'message': 'invalid_parameter', 'error_message': '[데이터]가(이) 유효하지 않습니다.'}  : 잘못된 요청값
                400, {'message': 'key_error', 'error_message': format(e)}                            : 잘못 입력된 키값
                500, {
                    'message': 'database_connection_fail',
                    'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                    }                                                                                : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러

            History:
                2020-01-04(김민구): 초기 생성

            Notes:
                type이 wait라면 미답변 Q&A만 보여주고 complete라면 답변 완료된 Q&A, all이라면 모든 Q&A를 보여준다.
        """

        connection = None
        try:
            data = {
                'type': args[0],
                'offset': args[1],
                'user_id': g.account_id
            }

            connection = get_connection(self.database)
            result = self.product_enquiry_list_service.my_page_enquiry_list_logic(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')