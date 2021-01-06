import traceback

from flask import g
from utils.decorator import signin_decorator
from utils.rules import SortTypeRule, NumberRule

from flask.views import MethodView
from flask import jsonify, request

from flask_request_validator import (
    validate_params,
    Param,
    GET
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail


class ProductDetailView(MethodView):
    def __init__(self, service, database):
        self.service  = service
        self.database = database
    
    @signin_decorator(False)
    def get(self, product_id):
        """ GET 메소드: 상품 상세정보 조회

         pass converter 로 받은 product_id 해당하는
         상품상세 정보를 조회 반환해준다.

        Args:

        Author: 김기용

        Returns:
            200, {'message': 'success', 'result': 상품정보}   
        
        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            500, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러
        History:

                2020-12-31(김기용): 초기 생성
                2021-01-01(김기용): 1차 구현
                2021-01-02(김기용): 북마크에대한 정보를 추가해주었다.
        """
        try:
            data=dict()
            data['product_id'] = product_id
            data['account_id'] = g.account_id
            connection = get_connection(self.database)
            result = self.service.product_detail_service(connection, data)
            return jsonify({'message': 'success', 'result': result})
        except Exception as e:
            raise e
        finally:
            if connection is not None:
                connection.close()


class ProductSearchView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
            Param('q', GET, str),
            Param('limit', GET, str, rules=[NumberRule()]),
            Param('sort_type', GET, str, rules=[SortTypeRule()])
            )
    def get(self, *args):
        """ GET 메소드: 상품 검색 

        사용자가 입력한 검색 키워드로 해당하는 상품이름,
        셀러이름을 조회해서반환해준다.

        Args:
            search   : 검색키워드
            limit    : 표시할 상품 개수
            sort_type: 정렬 종류(최신순, 판매순, 추천순)

        Author: 김기용

        Returns:
            200, {'message': 'success', 'result': 상품정보들}   
        
        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            500, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러
        History:

                2020-12-31(김기용): 초기 생성
                2021-01-01(김기용): 북마크에 대한 정보 추가
                2021-01-02(김기용): Param 값에대한 Rule을 정의해주었다.
        """

        connection = None
        try:

            data = {
                    'search': args[0],
                    'limit': int(args[1]),
                    'sort_type': args[2] 
                    }

            connection = get_connection(self.database)
            result = self.service.product_search_service(connection, data)
            return jsonify({'message': 'success', 'result': result})
        except Exception as e:
            raise e
        finally:
            if connection is not None:
                connection.close()


class ProductListView(MethodView):
    """ Presentation Layer

        Attributes:
            product_list_service : ProductListService 클래스
            database             : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-12-29(김민구): 초기 생성
            2020-12-31(김민구): 에러 문구 변경 / 하나의 이벤트에 대한 배너와 상품들을 반환하는 작업으로 수정
    """

    def __init__(self, services, database):
        self.product_list_service = services.product_list_service
        self.database = database

    @validate_params(
        Param('offset', GET, int, required=False, default=0),
        Param('limit', GET, int, required=False, default=30)
    )
    def get(self, *args):
        """ GET 메소드: 전체 상품 리스트 조회

            Args:
                offset = 0부터 시작
                limit = 30

            Author: 김민구

            Returns: 상품 리스트 조회 성공
                200, {
                        'message': 'success',
                        'result': {
                            "event": {
                                'id' : 1,
                                'banner_image' : 'url'
                            },
                            "product_list" : [
                                {
                                    'image': 'url',
                                    'seller_id': 1,
                                    'seller_name': '둘리',
                                    'product_id': 1,
                                    'product_name': '성보의 하루',
                                    'origin_price': 10000.0,
                                    'discount_rate': 0.1,
                                    'discounted_price': 9000.0,
                                    'sales_count': 30
                                },
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
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경 / 이벤트에 해당하는 상품 리스트 반환으로 수정

            Notes:
                offset을 받아서 한 페이지당 하나의 이벤트만 출력
                이벤트가 없을 시 빈 리스트 반환
        """

        connection = None
        try:
            data = {
                'offset': args[0],
                'limit': args[1]
            }
            connection = get_connection(self.database)
            result = self.product_list_service.product_list_logic(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            traceback.print_exc()
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')
