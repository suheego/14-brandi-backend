import traceback

from utils.custom_exceptions import DatabaseError, DataManipulationFail


class BookmarkDao:
    """ Persistence Layer

        Attributes: None

        Author: 김민구

        History:
            2020-01-02(김민구) 초기 생성
    """

    def get_bookmark_exist(self, connection, data):
        """ 해당 유저가 상품을 북마크 했는지 확인

        Args:
            connection : 데이터베이스 연결 객체
            data       : 서비스에서 넘겨 받은 dict ( product_id, account_id )

        Returns: 북마크 존재 유무를 반환
            1 : 해당 북마크가 존재
            0 : 해당 북마크가 존재하지 않음

        Raises:
            500, {'message': 'database_error', 'errorMessage': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

        History:
            2021-01-02(김민구): 초기 생성
        """

        sql = """
            SELECT
                EXISTS
                    (
                        SELECT 
                            id 
                        FROM 
                            bookmarks 
                        WHERE 
                            account_id = %(account_id)s 
                            AND product_id = %(product_id)s 
                            AND is_deleted = 0
                    );
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()[0]
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def create_bookmark(self, connection, data):
        """ 상품 북마크 추가

        Args:
            connection : 데이터베이스 연결 객체
            data       : 서비스에서 넘겨 받은 dict ( product_id, account_id )

        Returns:
            None

        Raises:
            500, {'message': 'database_error', 'errorMessage': '서버에 알 수 없는 에러가 발생했습니다.'}   : 데이터베이스 에러
            500, {'message': 'data_manipulation_fail', 'error_message': '북마크 추가를 실패하였습니다.'} : 데이터 조작 에러

        History:
            2021-01-02(김민구): 초기 생성
        """

        sql = """
            INSERT INTO bookmarks (
                account_id,
                product_id
            ) VALUES (
                %(account_id)s,
                %(product_id)s
            );
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DataManipulationFail('북마크 추가를 실패하였습니다.')

        except DataManipulationFail as e:
            raise e

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def delete_bookmark(self, connection, data):
        """ 상품 북마크 삭제

        Args:
            connection : 데이터베이스 연결 객체
            data       : 서비스에서 넘겨 받은 dict ( product_id, account_id )

        Returns:
            None

        Raises:
            500, {'message': 'database_error', 'errorMessage': '서버에 알 수 없는 에러가 발생했습니다.'}   : 데이터베이스 에러
            500, {'message': 'data_manipulation_fail', 'error_message': '북마크 삭제를 실패하였습니다.'} : 데이터 조작 에러

        History:
            2021-01-02(김민구): 초기 생성
        """

        sql = """
            UPDATE 
                bookmarks
            SET
                is_deleted = 1
            WHERE
                account_id = %(account_id)s
                AND product_id = %(product_id)s 
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DataManipulationFail('북마크 삭제를 실패하였습니다.')

        except DataManipulationFail as e:
            raise e

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def update_bookmark_volume_count(self, connection, data):
        """ 상품 북마크 수 업데이트

        Args:
            connection : 데이터베이스 연결 객체
            data       : 서비스에서 넘겨 받은 dict ( product_id, account_id, count )

        Returns:
            None

        Raises:
            500, {'message': 'database_error', 'errorMessage': '서버에 알 수 없는 에러가 발생했습니다.'}           : 데이터베이스 에러
            500, {'message': 'data_manipulation_fail', 'error_message': '북마크 추가 혹은 삭제를 실패하였습니다.'} : 데이터 조작 에러

        History:
            2021-01-02(김민구): 초기 생성
        """

        sql = """
            UPDATE
                bookmark_volumes
            SET 
                bookmark_count = bookmark_count + %(count)s
            WHERE
                product_id = %(product_id)s;
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DataManipulationFail('북마크 추가 혹은 삭제를 실패하였습니다.')

        except DataManipulationFail as e:
            raise e

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')