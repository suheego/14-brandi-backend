import traceback
import pymysql

from utils.custom_exceptions import (
    OrderNotExist,
    OrderCreateDenied,
    ProductNotExist,
    DeleteDenied,
    DeliveryMemoCreateDenied,
    OrderItemCreateDenied,
    ServerError,
    OrderHistoryCreateDenied,
    ProductRemainUpdateDenied,
)


class StoreOrderDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2020-12-30(고수희): 초기 생성
    """

    def get_store_order_dao(self, connection, data):
        """상품 결제 완료 결과 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            return

        Raises:
           400, {'message': 'order does not exist',
            'errorMessage': 'order_does_not_exist'} : 결제 상품 정보 조회 실패
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-30(고수희): 초기 생성
        """

        sql = """
        SELECT order_number, total_price
        FROM orders
        WHERE id = %s
        ; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data['order_id'])
                result = cursor.fetchone()
                if not result:
                    raise OrderNotExist('order_does_not_exist')
                return result

        except OrderNotExist as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def order_product_soldout_dao(self, connection, data):
        """상품 결제 시점에 해당 상품이 품절되었는지 여부 체크

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
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-30(고수희): 초기 생성
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
                    return {'sold_out': True}
                return {'sold_out': False}

        except ProductNotExist as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def post_delivery_type_dao(self, connection, data):
        """배송 정보 추가 (배송 메모가 직접 입력일 경우)

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 생성된 delivery_type_id 반환

        Raises:
            400, {'message': 'delivery memo create denied',
            'errorMessage': 'unable_to_create'} : 배송 정보 추가 실패
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-30(고수희): 초기 생성
        """

        sql = """
          INSERT INTO 
          delivery_memo_types (
          content
          ,is_default 
          ) VALUES (
          %(delivery_content)s
          ,0
          );
          """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.lastrowid
                if not result:
                    raise DeliveryMemoCreateDenied('unable_to_create')
                return result

        except DeliveryMemoCreateDenied as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def get_today_order_number_dao(self, connection):
        """주문번호 생성을 위한 당일 주문번호 채번

        Args:
            connection: 데이터베이스 연결 객체

        Author: 고수희

        Returns: 당일 주문량 +1

        History:
            2020-12-30(고수희): 초기 생성
        """

        # 같은 시점에 주문이 될 수 있음
        today_sql = """
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(today_sql)
                result = cursor.fetchone()
                return result

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def post_store_order_dao(self, connection, data):
        """주문 정보 추가

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 생성된 order_id 반환

        Raises:
            400, {'message': 'order create denied',
            'errorMessage': 'unable_to_create'} : 주문 정보 추가 실패
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-30(고수희): 초기 생성
        """
        sql = """
        INSERT INTO orders (
        order_number
        , sender_name
        , sender_phone
        , sender_email
        , recipient_name
        , recipient_phone
        , address1
        , address2
        , post_number
        , user_id
        , delivery_memo_type_id
        , total_price
        )
        VALUES (
        CONCAT(DATE_FORMAT(now(), '%%Y%%m%%d'),(LPAD(
        SELECT count(*)+1 as today
        FROM orders
        WHERE date(created_at) = date(now())
,6,0)),(LPAD(0,3,0)))
        , %(sender_name)s
        , %(sender_phone)s
        , %(sender_email)s
        , %(recipient_name)s
        , %(recipient_phone)s
        , %(address1)s
        , %(address2)s
        , %(post_number)s
        , %(user_id)s
        , %(delivery_memo_type_id)s
        , %(total_price)s
        );
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.lastrowid
                if not result:
                    raise OrderCreateDenied('unable_to_create')
                return result

        except OrderCreateDenied as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def post_store_order_item_dao(self, connection, data):
        """주문 상품 추가
        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 생성된 cart의 id 반환

        Raises:
            400, {'message': 'order item create denied',
            'errorMessage': 'unable_to_create'} : 주문 상품 추가 실패
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-30(고수희): 초기 생성
        """

        sql = """
          INSERT INTO order_items (
              product_id
              , stock_id
              , quantity
              , order_id
              , cart_id
              , order_detail_number
              , order_item_status_type_id
              , original_price
              , discounted_price
              , sale
          ) VALUES (
              %(product_id)s
              , %(stock_id)s
              , %(quantity)s
              , %(order_id)s
              , %(cart_id)s
              , CONCAT('B', DATE_FORMAT(now(), '%%Y%%m%%d'),(LPAD(%(today)s,6,0)),(LPAD(1,3,0)))
              , %(order_item_status_type_id)s
              , %(original_price)s
              , %(discounted_price)s
              , %(sale)s
          );
          """
        # insert로 꺼내서 넣
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.lastrowid
                if not result:
                    raise OrderItemCreateDenied('unable_to_create')
                return result

        except OrderItemCreateDenied as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server error')

    def post_store_order_item_history_dao(self, connection, data):
        """주문 상품 정보 이력 추가

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: None

        Raises:
            400, {'message': 'order history create denied',
            'errorMessage': 'unable_to_create'} : 주문 상품 정보 이력 추가 실패
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-30(고수희): 초기 생성
        """

        sql = """
        INSERT INTO order_item_histories (
            order_item_id
            , order_item_status_type_id
            , updater_id
        ) VALUES (
            %(order_item_id)s
            , %(order_item_status_type_id)s
            , %(user_id)s
        );
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.lastrowid
                if not result:
                    raise OrderHistoryCreateDenied('unable_to_create')

        except OrderHistoryCreateDenied as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server error')

    def patch_product_remain_dao(self, connection, data):
        """상품 재고 감소 처리

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: None

        Raises:
            400, {'message': 'product remain update denied',
            'errorMessage': 'unable_to_update'} : 상품 재고 업데이트 실패
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-31(고수희): 초기 생성
        """

        sql = """
        UPDATE stocks
        SET  remain = remain - %(quantity)s
        WHERE id = %(stock_id)s
        ;
        """

        try:
            with connection.cursor() as cursor:
                affected_row = cursor.execute(sql, data)
                if affected_row == 0:
                    raise ProductRemainUpdateDenied('unable_to_update')

        except ProductRemainUpdateDenied as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server error')

    def patch_is_delete_cart_item_dao(self, connection, data):
        """장바구니 상품 논리 삭제 처리

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: None

        Raises:
            400, {'message': 'invalid_delete_command_access',
            'errorMessage': 'unable_to_delete'} : 논리삭제 실패
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-31(고수희): 초기 생성
        """
        # 주문이 복수 아이템일 경우 Update join을 사용해서 삭제 처리
        sql = """
        UPDATE cart_items
        SET is_deleted = 1
        WHERE id = %(cart_id)s;
        """

        try:
            with connection.cursor() as cursor:
                affected_row = cursor.execute(sql, data)
                if affected_row == 0:
                    raise DeleteDenied('unable_to_delete')

        except DeleteDenied as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def patch_customer_information_dao(self, connection, data):
        """주문자 정보 추가 및 수정
        주문자 정보 조회 시 주문자 정보가 있으면 수정, 없으면 추가함

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: None

        Raises:
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-31(고수희): 초기 생성
        """

        sql = """
        INSERT INTO customer_information(
        account_id
        , name
        , email
        , phone
        )
        VALUES (
        %(user_id)s
        , %(sender_name)s
        , %(sender_email)s
        , %(sender_phone)s
        )
        ON DUPLICATE KEY UPDATE
        name = %(sender_name)s
        , email = %(sender_email)s
        , phone = %(sender_phone)s
        ;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)

        except Exception:
            traceback.print_exc()
            raise ServerError('server error')
