import json

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
    def __init__(self, services, database):
        self.product_list_service = services.product_list_service
        self.database = database

    @validate_params(
        Param('offset', GET, int)
    )
    def get(self, *args):
        """ GET 메소드: 전체 상품 리스트 조회

            Args:
                offset = 1부터 시작

            Author: 김민구

            Returns:
                200, {'message': 'success', 'result': result}                                       : 상품 리스트 조회 성공

            Raises:
                400, {'message': 'invalid_parameter', 'errorMessage': str(e)}                       : 잘못된 요청값
                400, {'message': 'key_error', 'errorMessage': format(e)}                            : 잘못 입력된 키값
                404, {'message': 'event_not_exist', 'errorMessage': '이벤트가 더 이상 존재하지 않습니다.'}   : 이벤트가 존재하지 않음
                500, {'message': 'database_connection_fail', 'errorMessage': 'database_close_fail'} : 커넥션 종료 실패
                500, {'message': 'database_error', 'errorMessage': format(e)}                       : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'errorMessage': format(e)})               : 서버 에러

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 수정 (이벤트에 해당하는 상품 리스트 반환으로 변경)

            Notes:
                result 리스트 안에 상품정보들과 이벤트 정보가 존재
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
