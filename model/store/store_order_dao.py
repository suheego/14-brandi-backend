import traceback
import pymysql

from utils.custom_exceptions import (
    OrderNotExist,
    OrderCreateDenied,
    AccountNotExist,
    ProductNotExist,
    DeleteDenied,
    DeliveryMemoCreateDenied,
    OrderItemCreateDenied,
    ServerError
)


class StoreOrderDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2020-12-30(고수희): 초기 생성
    """

    def get_user_permission_check_dao(self, connection, data):
        """사용자의 권한 조회

       Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 조회할 data

        Author:  고수희
        Returns: 조회된 권한 타입의 id 반환

        Raises:
            400, {'message': 'account_does_not_exist',
            'errorMessage': 'account_does_not_exist'} : 사용자 조회 실패

        History:
            2020-12-30(고수희): 초기 생성
        """

        sql = """
        SELECT permission_type_id
        FROM accounts  
        WHERE id = %s
        ;
        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data['user_id'])
                result = cursor.fetchone()
                if not result:
                    raise AccountNotExist('account_does_not_exist')
                return result

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def get_store_order_dao(self, connection, data):
        """상품 결제 완료 결과 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            return

        History:
            2020-12-30(고수희): 초기 생성

        Raises:
            400, {'message': 'order does not exist',
            'errorMessage': 'order_does_not_exist'} : 결제 상품 정보 조회 실패
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
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패

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

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def get_today_order_number_dao(self, connection):
        """주문번호 생성을 위한 당일 주문량 파악

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 생성된 order_id 반환

        Raises:
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 결 추가 실패

        History:
            2020-12-30(고수희): 초기 생성
        """

        today_sql = """
        SELECT count(*)+1 as today
        FROM orders
        WHERE date(created_at) = date(now())
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
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 주문 정보 추가 실패

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
        (CONCAT(DATE_FORMAT(now(), '%%y%%m%%d'),(LPAD(%(today)s,6,0)),LPAD(0,3,0))))
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
                result = cursor.lastrowid()
                if not result:
                    raise OrderCreateDenied('unable_to_create')
                return result

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
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패

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
              , %(order_detail_number)s
              , %(order_item_status_type_id)s
              , %(original_price)s
              , %(discounted_price)s
              , %(sale)s
          );
          """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.lastrowid
                if not result:
                    raise OrderItemCreateDenied('unable_to_create')
                return result
        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def post_store_order_item_history_dao(self, connection, data):
        """주문 상품 정보 이력 추가

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 생성된 cart의 id 반환

        Raises:
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패

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
            , %(updater_id)s
        );
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise CartItemCreateFail('unable_to_create')
            return result

    def post_store_order_item_status_dao(self, connection, data):
        """주문 상품 타입 추가

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 생성된 cart의 id 반환

        Raises:
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패

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
            , %(updater_id)s
        );
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise CartItemCreateFail('unable_to_create')
            return result

    def post_product_sales_rate_dao(self, connection, data):
        """주문한 상품 수량 만큼 상품 판매량 추가

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 생성된 cart의 id 반환

        Raises:
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패

        History:
            2020-12-31(고수희): 초기 생성
        """
        sql = """
        UPDATE customer_information
        SET
        `name` = %(`name`)s
        , email = %(email)s
        , phone = %(phone)s
        WHERE account_id = %(account_id)s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise CartItemCreateFail('unable_to_create')
            return result

    def post_patch_product_remain_dao(self, connection, data):
        """주문한 상품 수량 만큼 재고 감소 처리

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 생성된 cart의 id 반환

        Raises:
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패

        History:
            2020-12-31(고수희): 초기 생성
        """
        sql = """
        UPDATE customer_information
        SET
        `name` = %(`name`)s
        , email = %(email)s
        , phone = %(phone)s
        WHERE account_id = %(account_id)s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise CartItemCreateFail('unable_to_create')
            return result

    def post_is_delete_cart_item_dao(self, connection, data):
        """장바구니 상품 논리 삭제 처리

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: 논리 삭제 성공 여

        Raises:
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 논리삭 실패

        History:
            2020-12-31(고수희): 초기 생성
        """
        sql = """
        UPDATE cart_items
        SET is_deleted = 1
        WHERE id = %(cart_item_id)s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise DeleteDenied('unable_to_create')
            return result

    def post_customer_information_dao(self, connection, data):
        """주문자 정보 추가/수정

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 추가할 data

        Author: 고수희

        Returns: None

        Raises:
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패

        History:
            2020-12-31(고수희): 초기 생성
        """
        sql = """
        UPDATE customer_information
        SET
        `name` = %(`name`)s
        , email = %(email)s
        , phone = %(phone)s
        WHERE account_id = %(account_id)s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise CartItemCreateFail('unable_to_create')
            return result
