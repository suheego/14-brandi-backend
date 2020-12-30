import pymysql
from utils.custom_exceptions import CartItemNotExist, CartItemCreateFail, AccountNotExist, ProductNotExist


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
            return {totalPrice":"9000",
                        cartItem:
                            {id: 3,
                            "sellerName": "미우블랑",
                            "productId": 3,
                            "productName": "회색 반팔티",
                            "productImage": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
                            "stockId": 3,
                            "size": "Free",
                            "color": "Gray",
                            "quantity": 1,
                            "sale": 10,
                            "originalPrice": 10000,
                            "discountedPrice": 9000,
                        }}

        History:
            2020-12-28(고수희): 초기 생성

        Raises:
            400, {'message': 'cart item does not exist',
            'errorMessage': 'cart_item_does_not_exist'} : 장바구니 상품 정보 조회 실패
        """
        sql = """
        SELECT 
        ct.id as id
        , se.name as sellerName
        , ct.product_id as productId
        , pd.name as productName
        , pi.image_url as image
        , ct.stock_id as stockId
        , co.name as color
        , sz.name as size
        , ct.quantity as quantity
        , CONVERT(ct.sale*100, UNSIGNED) as sale
        , CONVERT(ct.original_price, UNSIGNED) as originalPrice
        , CONVERT(ct.discounted_price, UNSIGNED) as discountedPrice 
        FROM cart_items as ct
        INNER JOIN stocks as st ON st.id = stock_id
        INNER JOIN colors as co ON co.id = st.color_id
        INNER JOIN sizes as sz ON sz.id = st.size_id
        INNER JOIN product_images as pi ON pi.product_id = ct.product_id AND pi.order_index = 1
        INNER JOIN products as pd ON pd.id = ct.product_id 
        INNER JOIN sellers as se ON se.account_id = pd.seller_id
        WHERE ct.id = %s
        AND ct.is_deleted = 0
        ; 

        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data['cart_id'])
            item_info = cursor.fetchone()
            if not item_info:
                raise CartItemNotExist('cart_item_does_not_exist')
            result = {"totalPrice": (item_info['discountedPrice']
                                     if item_info['discountedPrice'] > 0
                                     else item_info['originalPrice']), "cartItem": item_info}
            return result

    def get_cart_item_soldout_dao(self, connection, data):
        """장바구니 상품 조회 시점에 해당 상품이 품절되었는지 여부 체크

        Args:
            connection  : 데이터베이스 연결 객체
            data        : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            {'soldOut': true}: 상품이 품절됨
            {'soldOut': falue}: 상품이 품절되지 않음

        Raises:
            400, {'message': 'cart item does not exist',
            'errorMessage': 'cart_item_does_not_exist'} : 장바구니 상품 정보 조회 실패

        History:
            2020-12-29(고수희): 초기 생성
        """

        sql = """
        SELECT st.remain as remain
        FROM cart_items as ct
        INNER JOIN stocks as st ON st.id = stock_id
        WHERE ct.id = %s
        AND ct.is_deleted = 0
        ;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data['cart_id'])
            result = cursor.fetchone()
            if not result:
                raise CartItemNotExist('cart_item_does_not_exist')

            #상품 재고가 0인지 확인하여, 상품이 품절되었는지 체크
            if result['remain'] <= 0:
                return {'soldOut': True}
            return {'soldOut': False}

    def get_user_permission_check_dao(self, connection, data):
        """사용자의 권한 조회

       Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 조회할 data

        Author:  고수희
        Returns: 조회된 권한 타입의 id 반환

        Raises:
            400, {'message': 'accont_does_not_exist',
            'errorMessage': 'account_does_not_exist'} : 사용자 조회 실패

        History:
            2020-12-29(고수희): 초기 생성
        """

        sql = """
        SELECT permission_type_id
        FROM accounts  
        WHERE id = %s
        ;
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data['user_id'])
            result = cursor.fetchone()
            if not result:
                raise AccountNotExist('account_does_not_exist')
            return result

    def product_soldout_dao(self, connection, data):
        """장바구니 상품 추가 시점에 해당 상품이 품절되었는지 여부 체크

        Args:
            connection  : 데이터베이스 연결 객체
            data        : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            {'soldOut': true}: 상품이 품절됨
            {'soldOut': false}: 상품이 품절되지 않음

        Raises:
            400, {'message': 'cart item does not exist',
            'errorMessage': 'cart_item_does_not_exist'} : 장바구니 상품 정보 조회 실패

        History:
            2020-12-29(고수희): 초기 생성
        """
        sql = """
        SELECT st.remain as remain
        FROM products as pd
        INNER JOIN stocks as st ON st.id = pd.id
        WHERE pd.id = %s
        ;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data['product_id'])
            result = cursor.fetchone()
            if not result:
                raise ProductNotExist('product_does_not_exist')

            #상품 재고가 0인지 확인하여, 상품이 품절되었는지 체크
            if result['remain'] <= 0:
                return {'soldOut': True}
            return {'soldOut': False}

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
                raise CartItemCreateFail('unable_to_create')
            return result
