import pymysql
from utils.custom_exceptions import UserUpdateDenied, UserCreateDenied, UserNotExist


class CartItemDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2020-12-28(고수희): 고수희
    """

    def get_cart_item(self, connection, cart_ids):
        cart_id = cart_ids
        """장바구니 상품 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            cart_id   : 서비스 레이어에서 넘겨 받은 수정할 cart_id

        Author: 고수희

        Returns:
            return [{'id': 12, 'name': '김기용', 'gender': '남자', 'age': '18'}]

        History:
            2020-12-28(고수): 초기 생성

        Raises:
            400, {'message': 'user dose not exist', 'errorMessage': 'user_does_not_exist'} : 유저 정보 조회 실패
        """

        sql = """
            SELECT * 
            FROM users
            WHERE id=%s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, cart_id)
            result = cursor.fetchall()
            if not result:
                raise UserNotExist('user_does_not_exist')
            return result

    def post_dao(self, connection, data):
        """장바구니  생성

        Args:
            connection: 데이터베이스 연결 객체
            data      : service 에서 넘겨 받은 dict 객체

        Author: 고수희

        Returns:
            return (): 생성 성공

        Raises:
            400, {'message': 'unable to create', 'errorMessage': 'unable_to_create'} : 유저 생성 실패

        History:
            2020-12-28(고수희): 초기 생성
        """
        sql = """
        INSERT INTO users 
        (
            name,
            gender,
            age
        )
        VALUES(
            %(name)s,
            %(gender)s,
            %(age)s
            );
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise UserCreateDenied('unable_to_create')
            return result
