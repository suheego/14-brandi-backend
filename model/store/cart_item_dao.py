import traceback
import pymysql
from utils.custom_exceptions import (
    CartItemNotExist,
    CartItemCreateDenied,
    AccountNotExist,
    ProductNotExist,
    ServerError
)


class CartItemDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2020-12-28(고수희): 초기 생성
            2021-01-02(고수희): traceback 추가
    """
    def get_cart_item_dao(self, connection, data):
        """장바구니 상품 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
                "result": {
                    "cart_item": {
                        "color": "Black",
                        "discounted_price": 9000.0,
                        "id": 23,
                        "image_url": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
                        "original_price": 14000.0,
                        "product_id": 1,
                        "product_name": "성보의하루1",
                        "quantity": "1",
                        "sale": 0.1,
                        "seller_name": "나는셀러9",
                        "size": "Free",
                        "soldout": false,
                        "stock_id": 1,
                        "total_price": 9000.0
                    }
                }

        History:
            2020-12-28(고수희): 초기 생성
            2021-01-01(고수희): 상품 조회 시 재고도 함께 조회하는 것으로 로직 수정
            2021-01-02(고수희): traceback 추가

        Raises:
            400, {'message': 'cart item does not exist',
            'errorMessage': 'cart_item_does_not_exist'} : 장바구니 상품 정보 조회 실패
        """

        sql = """
        SELECT 
        ct.id 
        , se.name AS seller_name
        , ct.product_id 
        , pd.name AS product_name
        , pi.image_url
        , ct.stock_id 
        , co.name AS color
        , sz.name AS size
        , ct.quantity 
        , sale
        , ct.original_price 
        , ct.discounted_price 
        , st.remain AS soldout
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

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data['cart_id'])
                item_info = cursor.fetchone()
                if not item_info:
                    raise CartItemNotExist('cart_item_does_not_exist')

                # 상품 재고가 0인지 확인하여, 상품이 품절되었는지 체크
                if item_info['soldout'] <= 0:
                    item_info['soldout'] = True
                item_info['soldout'] = False

                # 총 가격 계산, 할인가가 있으면 할인가가 총 가격이 됨
                total_price = {"total_price": (item_info['discounted_price']
                                              if item_info['discounted_price'] > 0
                                              else item_info['original_price'])}

                #총 가격을 상품 조회 결과에 병합
                item_info.update(total_price)
                result = {"cart_item": item_info}

                return result

        except CartItemNotExist as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

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
            400, {'message': 'product does not exist',
            'errorMessage': 'product_does_not_exist'} : 상품을 조회할 수 없음

        History:
            2020-12-29(고수희): 초기 생성
            2021-01-02(고수희): traceback 추가
        """
        sql = """
        SELECT st.remain as remain
        FROM products as pd
        INNER JOIN stocks as st ON st.id = pd.id
        WHERE pd.id = %s
        ;
        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data['product_id'])
                result = cursor.fetchone()
                if not result:
                    raise ProductNotExist('product_does_not_exist')

                #상품 재고가 0인지 확인하여, 상품이 품절되었는지 체크
                if result['remain'] <= 0:
                    return {'soldout': True}
                return {'soldout': False}

        except ProductNotExist as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def post_cart_item_dao(self, connection, data):
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
            2021-01-02(고수희): traceback 추가
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
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.lastrowid
                if not result:
                    raise CartItemCreateDenied('unable_to_create')
                return result

        except CartItemCreateDenied as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')
