from flask.views import MethodView
from flask import jsonify

from flask_request_validator import (
    validate_params,
    Param,
    GET
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail


class ProductListView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('offset', GET, int),
        Param('limit', GET, int)
    )
    def get(self, *args):
        """ GET 메소드: 전체 상품 리스트 조회

            Args:
                offset = 0부터 30단위로 변경
                limit = 고정값 30

            Author: 김민구

            Returns:
                200, {'message': 'success', 'result': result}                                       : 상품 리스트 조회 성공

            Raises:
                400, {'message': 'invalid_parameter', 'errorMessage': str(e)}                       : 잘못된 요청값
                400, {'message': 'key_error', 'errorMessage': format(e)}                            : 잘못 입력된 키값
                500, {'message': 'database_connection_fail', 'errorMessage': 'database_close_fail'} : 커넥션 종료 실패
                500, {'message': 'database_error', 'errorMessage': format(e)}                       : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'errorMessage': format(e)})               : 서버 에러

            History:
                2020-20-30(김민구): 초기 생성

            Notes:
                offset = 0부터 30단위로 올라감
                limit = 30 고정값

                상품 리스트 20개당 이벤트 배너 1개씩 조회
                offset이 0 혹은 20의 배수일 때는 event 배너가 1개
                20의 배수가 아닐 때는 event 배너가 2개

                ex) offset 0,  limit = 30 : product 1번부터~30번 (20)
                            event 배너 1개(1), event_offset = 0, event_limit = 1

                        offset 30, limit = 30 : product 31번부터 60번 (40, 60)
                            event 배너 2개(2,3), event_offset = 1, event_limit = 2

                        offset 60, limit = 30 : product 61번부터 90번 (80)
                            event 배너 1개(4), event_offset = 3, event_limit = 1

                        offset 90, limit = 30 : product 91번부터 120번 (100, 120)
                            event 배너 2개(5,6), event_offset = 4, event_limit = 2
        """

        try:
            data = {
                "offset": args[0],
                "limit": args[1]
            }
            connection = get_connection(self.database)
            result = self.service.product_list_service(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database_close_fail')


class CategoryListView(MethodView):
    """ GET 메소드: 전체 카테고리 리스트 조회

        Args:
            None

        Author: 김민구

        Returns:
            200, {'message': 'success', 'result': result}                                       : 카테고리 리스트 조회 성공

        Raises:
            400, {'message': 'key_error', 'errorMessage': format(e)}                            : 잘못 입력된 키값
            500, {'message': 'database_connection_fail', 'errorMessage': 'database_close_fail'} : 커넥션 종료 실패
            500, {'message': 'database_error', 'errorMessage': format(e)}                       : 데이터베이스 에러
            500, {'message': 'internal_server_error', 'errorMessage': format(e)})               : 서버 에러

        History:
            2020-20-30(김민구): 초기 생성

        Notes:
            menus, main_category, sub_category 총 3가지의 카테고리가 result 키의 값으로 반환
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    def get(self):
        try:
            connection = get_connection(self.database)
            result = self.service.category_list_service(connection)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database_close_fail')