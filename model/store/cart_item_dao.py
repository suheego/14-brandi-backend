import pymysql
from utils.custom_exceptions import CartItemNotExist, CartItemCreateDenied, CartItemUpdateDenied


class CartItemDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2020-12-28(고수희): 초기 생성
    """

    def get_dao(self, connection, data):
        """장바구니 상품 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            return [{"id":"3",
                    "product_id": "3",
                    "stock_id": "41",
                    "quantity": "1",
                    "sale":"0.10",
                    "origin_price":"10000",
                    "discounted_price":"9000"
                    }]

        History:
            2020-12-28(고수희): 초기 생성

        Raises:
            400, {'message': 'cart item does not exist',
            'errorMessage': 'cart_item_does_not_exist'} : 유저 정보 조회 실패
        """
        sql = """
        SELECT 
        id
        , product_id
        , stock_id
        , quantity
        , user_id
        , sale
        , original_price
        , discounted_price
        FROM 
        cart_items
        WHERE 
        cart_id = $(cart_id)s
        AND is_deleted = 0;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, cart_id)
            result = cursor.fetchall()
            if not result:
                raise CartItemNotExist('cart_item_does_not_exist')
            return result

    def post_dao(self, connection, data):
        """장바구니 상품 추가

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 홍길동

        Returns: None

        Raises:
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패

        History:
            2020-12-28(고수희): 초기 생성
        """
        sql = """
        INSERT INTO
        cart_items (
        product_id
        , stock_id
        , quantity
        , user_id
        , sale
        , original_price
        , discounted_price
        ) 
        VALUES (
        %(product_id)s
        , %(stock_id)s
        , %(quantity)s
        , %(user_id)s
        , %(sale)s
        , %(original_price)s
        , %(discounted_price)s
        );
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise CartItemCreateDenied('unable_to_create')
            return result

    # def patch_dao(self, connection, data):
    #     """장바구니 상품 수량 수정
    #
    #     Args:
    #         connection: 데이터베이스 연결 객체
    #         data      : 서비스 레이어에서 넘겨 받아 추가할 data
    #
    #     Author: 고수희
    #
    #     Returns: None
    #
    #     Raises:
    #         400, {'message': 'unable to update',
    #         'errorMessage': 'unable_to_update'} : 장바구니 상품 수량 수정 실패
    #
    #     History:
    #         2020-12-28(고수희): 초기 생성
    #     """
    #     sql = """
    #     BEGIN TRANSACTION
    #
    #     INSERT INTO
    #     cart_items (
    #     product_id
    #     , stock_id
    #     , quantity
    #     , user_id
    #     , sale
    #     , original_price
    #     , discounted_price
    #     )
    #     VALUES (
    #     %(product_id)s
    #     , %(stock_id)s
    #     , %(quantity)s
    #     , %(user_id)s
    #     , %(sale)s
    #     , %(original_price)s
    #     , %(discounted_price)s
    #     );
    #
    #     UPDATE
    #     cart_items
    #     SET
    #     quantity = quantity + %(quantity)s
    #     WHERE
    #     product_id = %(product_id)s
    #     AND
    #     user_id = %(user_id)s
    #     ;
    #     """
    #
    #     print(data)
    #     print(sql)
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql, data)
    #         result = cursor.lastrowid
    #         if not result:
    #             raise CartItemUpdateDenied('unable_to_update')
    #         return result