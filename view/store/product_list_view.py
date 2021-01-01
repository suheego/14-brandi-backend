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

    def get(self):
        pass


class ProductSearchView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    def get(self):
        """ GET 메소드: 상품 검색 
        """
        try:
            search = request.args.get('q')
            connection = get_connection(self.database)
            result = self.service.product_search_service(connection, search)
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
        Param('offset', GET, int)
    )
    def get(self, *args):
        """ GET 메소드: 전체 상품 리스트 조회

            Args:
                offset = 0부터 시작

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
            offset = args[0]
            connection = get_connection(self.database)
            result = self.product_list_service.product_list_logic(connection, offset)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')
