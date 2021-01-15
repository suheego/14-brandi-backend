import traceback

from flask.views import MethodView
from flask import jsonify

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail


class CategoryListView(MethodView):
    """ Presentation Layer

        Attributes:
            category_list_service : CategoryListService 클래스
            database              : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-12-29(김민구): 초기 생성
    """

    def __init__(self, services, database):
        self.category_list_service = services.category_list_service
        self.database = database

    def get(self):
        """ GET 메소드: 전체 카테고리 리스트 조회

            Author: 김민구

            Returns: 카테고리 리스트 조회 성공
                200, {
                        'message': 'success',
                        'result': {
                            'menus': [
                                {
                                    'id' : 1,
                                    'name' : '브랜드'
                                    'main_categories': [
                                        {
                                            'id' : 1,
                                            'name' : '상의',
                                            'menu_id' : 6
                                            'sub_categories': [
                                                {
                                                    'id' : 1,
                                                    'name' : '반팔티셔츠',
                                                    'main_categories' : 1
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                }

            Raises:
                400, {'message': 'key_error', 'errorMessage': format(e)}                            : 잘못 입력된 키값
                500, {
                        'message': 'database_connection_fail',
                        'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                    }                                                                               : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})              : 서버 에러

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경

            Notes:
                menus, main_category, sub_category 총 3가지의 카테고리가 result 키의 값으로 반환
        """

        connection = None
        try:
            connection = get_connection(self.database)
            result = self.category_list_service.category_list_logic(connection)
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
