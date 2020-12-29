import pymysql
from utils.custom_exceptions import CartItemNotExist, CartItemCreateDenied, CartItemUpdateDenied


class CartItemDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2020-12-28(고수희): 초기 생성
    """

    def get_dao(self, connection, cart_id):
        cart_id = cart_id
        """장바구니 상품 정보 조회, 장바구니 상품 조회 시점에 상품이 품절되었는지 여부 체크

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            return {totalPrice":"9000",
                       {id": "3",
                        "sellerName": "미우블랑"
                        "productName": "회색 반팔티"
                        "productImage": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
                        "productSize": "Free"
                        "productColor": "Gray"
                        "quantity": "1",
                        "sale": "0.10",
                        "originalPrice": "10000",
                        "discountedPrice": "9000"
                        }}

        History:
            2020-12-28(고수희): 초기 생성

        Raises:
            400, {'message': 'cart item does not exist',
            'errorMessage': 'cart_item_does_not_exist'} : 장바구니 상품 정보 조회 실패
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
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, cart_id)
            result = cursor.fetchall()
            if not result:
                raise CartItemNotExist('cart_item_does_not_exist')
            return result

    def get_cart_item_soldout_dao(self, connection, cart_id):
        """장바구니 상품 조회 시점에 상품이 품절되었는지 여부 체크

        Args:
            connection  : 데이터베이스 연결 객체
            cart_id     : 서비스 레이어에서 넘겨 받아 조회할 cart_id

        Author: 고수희

        Returns: None

        Raises:
            400, {'message': 'cart item does not exist',
            'errorMessage': 'cart_item_does_not_exist'} : 장바구니 상품 정보 조회 실패

        History:
            2020-12-29(고수희): 초기 생성
        """

        sql = """
        SELECT
        *
        FROM 
        cart_items
        WHERE 
        id = %s
        ;
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

        Author: 고수희

        Returns: 생성된 cart의 id 반환

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
