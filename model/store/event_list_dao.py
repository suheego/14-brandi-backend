import pymysql

from utils.custom_exceptions import DatabaseError


class EventListDao:
    """ Persistence Layer

        Attributes: None

        Author: 김민구

        History:
            2020-01-01 초기 생성
    """

    def get_event_banner_list(self, connection, data):
        """ 기획전의 아이디와 배너를 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict (offset, limit, is_proceeding)

            Returns: 해당 기획전 배너 30개 반환
                [
                    {
                        "event_banner_image": "url"
                        "event_id": 1,
                        "event_kind_id": 1,
                        "event_type_id": 1
                    }
                ]

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2021-01-01(김민구): 초기 생성
        """

        sql = """
            SELECT 
                `event`.id AS event_id
                , `event`.banner_image AS event_banner_image
                , `event`.event_type_id
                , `event`.event_kind_id
            FROM 
                `events` AS `event`
            WHERE 
                `event`.is_display = 1
                AND `event`.is_deleted = 0
                AND IF(
                    %(is_proceeding)s = 0,
                    now() > `event`.end_date,
                    now() < `event`.end_date
                )
            ORDER BY 
                `event`.id ASC  
            LIMIT %(offset)s, %(limit)s; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event_information(self, connection, event_id):
        """ 기획전의 정보를 조회

            Args:
                connection : 데이터베이스 연결 객체
                event_id   : 서비스에서 넘겨 받은 int

            Returns: 해당 기획전 정보 반환
              {
                    "detail_image": "url"
                    "event_id": 1,
                    "event_kind_id": 1,
                    "event_kind_name": "상품",
                    "event_type_id": 1,
                    "event_type_name": "상품(이미지)",
                    "is_button": 0
                }

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2021-01-01(김민구): 초기 생성

            Notes:
                해당 기획전의 정보를 반환
                is_button으로 버튼 유무를 판별
        """

        sql = """
            SELECT
                `event`.id AS event_id
                , `event`.detail_image
                , `event`.event_type_id
                , event_type.`name` AS event_type_name
                , `event`.event_kind_id
                , event_kind.`name` AS event_kind_name
                , (
                    CASE `event`.event_kind_id
                        WHEN 2 THEN 1
                        ELSE 0
                    END
                ) AS is_button
            FROM 
                `events` AS `event`
                INNER JOIN event_types AS event_type
                    ON event_type.id = `event`.event_type_id
                INNER JOIN event_kinds AS event_kind
                    ON event_kind.id = `event`.event_kind_id
            WHERE
                `event`.id = %s
                AND `event`.is_display = 1
                AND `event`.is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, event_id)
                result = cursor.fetchone()
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event_button(self, connection, event_id):
        """ 기획전의 버튼을 조회

            Args:
                connection : 데이터베이스 연결 객체
                event_id   : 서비스에서 넘겨 받은 int

            Returns: 해당 기획전의 모든 버튼을 반환
                [
                    {
                        "event_id": 2,
                        "id": 1,
                        "name": "1번 버튼",
                        "order_index": 1
                    }
                ]

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2021-01-01(김민구): 초기 생성

            Notes:
                해당 기획전의 버튼을 반환
        """

        sql = """
            SELECT
                id
                , `name`
                , order_index
                , event_id
            FROM 
                event_buttons
            WHERE
                event_id = %s
                AND is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, event_id)
                result = cursor.fetchall()
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def is_event_has_button(self, connection, event_id):
        """ 기획전의 버튼 유무를 조회

            Args:
                connection : 데이터베이스 연결 객체
                event_id   : 서비스에서 넘겨 받은 int

            Returns:
                0 : 버튼이 없음
                1 : 버튼이 있음

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2021-01-01(김민구): 초기 생성

            Notes:
                해당 기획전의 버튼 유무를 반환
        """

        sql = """
            SELECT
                (
                    CASE event_kind_id
                        WHEN 2 THEN 1
                        ELSE 0
                    END
                ) AS is_button
            FROM 
                `events`
            WHERE
                id = %s
                AND is_display = 1
                AND is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, event_id)
                result = cursor.fetchone()
                return result['is_button']

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event_button_product_list(self, connection, data):
        """ 버튼 기획전의 상품 리스트를 반환

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict ( offset, limit, event_id )

            Returns: 30개의 상품을 반환
                [
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "event_button_id": 3,
                        "image_url": "url",
                        "origin_price": 10000.0,
                        "product_id": 249,
                        "product_name": "성보의하루249",
                        "sales_count": 94,
                        "seller_name": "나는셀러2"
                    }
                ]

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2021-01-01(김민구): 초기 생성

            Notes:
                해당 버튼 기획전의 상품 리스트를 반환
        """

        sql = """
            SELECT 
                product.id AS product_id
                , product_image.image_url
                , seller.`name` AS seller_name
                , product.`name` AS product_name
                , product.origin_price
                , product.discount_rate
                , product.discounted_price
                , product_sales_volume.sales_count
                , events_product.event_button_id
            FROM
                events_products AS events_product
                INNER JOIN products AS product
                    ON product.id = events_product.product_id
                INNER JOIN product_images AS product_image
                    ON product.id = product_image.product_id AND product_image.order_index = 1
                INNER JOIN sellers AS seller
                    ON seller.account_id = product.seller_id
                INNER JOIN product_sales_volumes AS product_sales_volume
                    ON product_sales_volume.product_id = product.id
            WHERE
                events_product.event_id = %(event_id)s
                AND product.is_deleted = 0
                AND product.is_display = 1
            ORDER BY
                product.id DESC
            LIMIT %(offset)s, %(limit)s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event_product_list(self, connection, data):
        """ 기획전의 상품 리스트를 반환

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict ( offset, limit, event_id )

            Returns: 30개의 상품을 반환
                [
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "image_url": "url",
                        "origin_price": 10000.0,
                        "product_id": 249,
                        "product_name": "성보의하루249",
                        "sales_count": 94,
                        "seller_name": "나는셀러2"
                    }
                ]

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2021-01-01(김민구): 초기 생성

            Notes:
                해당 기획전의 상품 리스트를 반환
        """

        sql = """
            SELECT 
                product.id AS product_id
                , product_image.image_url
                , seller.`name` AS seller_name
                , product.`name` AS product_name
                , product.origin_price
                , product.discount_rate
                , product.discounted_price
                , product_sales_volume.sales_count
            FROM
                events_products AS events_product
                INNER JOIN products AS product
                    ON product.id = events_product.product_id
                INNER JOIN product_images AS product_image
                    ON product.id = product_image.product_id AND product_image.order_index = 1
                INNER JOIN sellers AS seller
                    ON seller.account_id = product.seller_id
                INNER JOIN product_sales_volumes AS product_sales_volume
                    ON product_sales_volume.product_id = product.id
            WHERE
                events_product.event_id = %(event_id)s
                AND product.is_deleted = 0
                AND product.is_display = 1
            ORDER BY
                product.id DESC
            LIMIT %(offset)s, %(limit)s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')
