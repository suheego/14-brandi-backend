from flask.views import MethodView
from flask import jsonify, g

from flask_request_validator import (
    validate_params,
    Param,
    PATH
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.decorator import signin_decorator


class BookmarkView(MethodView):
    """ Presentation Layer

        Attributes:
            bookmark_service   : BookmarkService 클래스
            database           : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-01-02(김민구): 초기 생성
    """

    def __init__(self, services, database):
        self.bookmark_service = services.bookmark_service
        self.database = database

    @signin_decorator()
    @validate_params(
        Param('product_id', PATH, int)
    )
    def post(self, *args):
        """ POST 메소드: 북마크 추가

        Args:
            product_id = 상품 아이디

        Author: 김민구

        Returns:
            200, {'message': 'success'}

        Raises:
            400, {'message': 'key_error', 'error_message': format(e)}                                : 잘못 입력된 키값
            400, {'message': 'already_exist_bookmark', 'error_message': '이미 추가된 북마크입니다.'}        : 북마크 중복
            500, {
                'message': 'database_connection_fail',
                'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                }                                                                                    : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'data_manipulation_fail', 'error_message': '북마크 추가를 실패하였습니다.'} : 데이터 조작 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러
        """

        connection = None
        try:
            data = {
                'product_id': args[0],
                'account_id': g.account_id
            }
            connection = get_connection(self.database)
            self.bookmark_service.post_bookmark_logic(connection, data)
            connection.commit()
            return jsonify({'message': 'success'}), 200

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')

    @signin_decorator()
    @validate_params(
        Param('product_id', PATH, int)
    )
    def delete(self, *args):
        """ DELETE 메소드: 북마크 삭제

        Args:
            product_id = 상품 아이디

        Author: 김민구

        Returns:
            200, {'message': 'success'}

        Raises:
            400, {'message': 'key_error', 'error_message': format(e)}                                : 잘못 입력된 키값
            400, {'message': 'not_exist_bookmark', 'error_message': '해당 북마크가 존재하지 않습니다.'}       : 존재하지 않는 북마크
            500, {
                'message': 'database_connection_fail',
                'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                }                                                                                    : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'data_manipulation_fail', 'error_message': '북마크 삭제를 실패하였습니다.'} : 데이터 조작 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러
        """

        connection = None
        try:
            data = {
                'product_id': args[0],
                'account_id': g.account_id
            }
            connection = get_connection(self.database)
            self.bookmark_service.delete_bookmark_logic(connection, data)
            connection.commit()
            return jsonify({'message': 'success'}), 200

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')
