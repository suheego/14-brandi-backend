import pymysql
from utils.custom_exceptions import EventDoesNotExist


class EventDao:
    """ Persistence Layer

        Attributes: None

        Author: 강두연

        History:
            2020-12-28(강두연): 초기 생성 및 조회 기능 작성
            2020-12-29(강두연): 이벤트 검색조건별 조회 작성
            2020-12-30(강두연): 이벤트 상세정보 및 수정페이지 기능 작성
    """

    def get_events_list(self, connection, data):
        """기획전 정보 조회

            Args:
                connection: 데이터베이스 연결 객체
                data   : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Author: 강두연

            Returns:
                {
                    "events": [
                        {
                            "created_at": "2020-12-28 16:40:41",
                            "end_date": "2021-03-01 00:00:00",
                            "event_kind": "버튼",
                            "event_name": "성보의 하루 시리즈2(버튼형)",
                            "event_number": 2,
                            "event_status": "진행중",
                            "event_type": "상품(이미지)",
                            "is_display": "노출",
                            "product_count": 59,
                            "start_date": "2020-10-19 00:00:00"
                        },
                        {
                            "created_at": "2020-12-28 16:40:41",
                            "end_date": "2021-03-01 00:00:00",
                            "event_kind": "상품",
                            "event_name": "성보의 하루 시리즈",
                            "event_number": 1,
                            "event_status": "진행중",
                            "event_type": "상품(이미지)",
                            "is_display": "노출",
                            "product_count": 40,
                            "start_date": "2020-10-19 00:00:00"
                        }
                    ],
                    "total_count": 2
                }

            History:
                2020-12-28(강두연): 초기 생성 및 조회 기능 작성
                2020-12-29(강두연): 이벤트 검색조건별 조회 작성
                2020-12-30(강두연): 조회된 이벤트 총 갯수 반환기능 작성
            Raises:
                404, {'message': 'event not exist', 'errorMessage': 'event does not exist'} : 이벤트 정보 조회 실패
        """

        total_count_sql = """
            SELECT
                COUNT(*) AS total_count
        """

        sql = """
            SELECT
                `event`.id AS event_number
                , `event`.`name` AS event_name
                , CASE WHEN NOW() BETWEEN `event`.start_date AND `event`.end_date THEN '진행중'
                     WHEN NOW() < `event`.start_date THEN '대기'
                     ELSE '종료' END AS event_status
                , event_type.`name` AS event_type
                , event_kind.`name` AS event_kind
                , `event`.start_date AS start_date
                , `event`.end_date AS end_date
                , CASE WHEN `event`.is_display = 0 THEN '비노출' ELSE '노출' END AS is_display
                , `event`.created_at AS created_at
                , (SELECT COUNT(CASE WHEN events_products.event_id = `event`.id THEN 1 END)
                    FROM events_products) AS product_count
            """

        extra_sql = """
            FROM `events` AS `event`
                INNER JOIN event_types AS event_type
                    ON `event`.event_type_id = event_type.id
                INNER JOIN event_kinds AS event_kind
                   ON `event`.event_kind_id = event_kind.id
            WHERE
                `event`.is_deleted = 0
        """

        # search option 1 : search by keyword (event_name or event_number)
        if data['name']:
            extra_sql += ' AND `event`.`name` LIKE %(name)s'
        elif data['number']:
            extra_sql += ' AND `event`.id = %(number)s'

        # search option 2 : search by event_status
        if data['status'] == 'progress':
            extra_sql += ' AND NOW() BETWEEN `event`.start_date AND `event`.end_date'
        elif data['status'] == 'wait':
            extra_sql += ' AND NOW() < `event`.start_date'
        elif data['status'] == 'end':
            extra_sql += ' AND NOW() > `event`.end_date'

        # search option 3 : exposure
        if data['exposure'] is not None and data['exposure']:
            extra_sql += ' AND `event`.is_display = 1'
        elif data['exposure'] is not None and not data['exposure']:
            extra_sql += ' AND `event`.is_display = 0'

        # search option 4 : event_registered_date
        if data['start_date'] and data['end_date']:
            extra_sql += """
                AND `event`.created_at BETWEEN CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """

        sql += extra_sql
        total_count_sql += extra_sql
        sql += ' ORDER BY `event`.id DESC LIMIT %(page)s, %(length)s;'

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            events = cursor.fetchall()
            if not events:
                raise EventDoesNotExist('event does not exist')
            cursor.execute(total_count_sql, data)
            count = cursor.fetchone()
            return {'events': events, 'total_count': count['total_count']}

    def get_event_detail(self, connection, data):
        """ 기획전 상세 정보 조회 (수정페이지)

            Args:
                connection: 데이터베이스 연결 객체
                data   : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Author: 강두연

            Returns: {
                "banner_image": "https://images.url.com",
                "detail_image": "https://images.url.com",
                "end_date": "2021-03-01 00:00:00",
                "event_id": 1,
                "event_kind": "상품",
                "event_name": "성보의 하루 시리즈",
                "event_type": "상품(이미지)",
                "is_display": 1,
                "start_date": "2020-10-19 00:00:00"
            }

            History:
                2020-12-30(강두연): 초기 생성
        """

        sql = """
            SELECT
                `event`.id AS event_id
                , `event`.`name` AS event_name
                , event_type.`name` AS event_type
                , event_type.id AS event_type_id
                , event_kind.`name` AS event_kind
                , event_kind.id AS event_kind_id
                , `event`.is_display AS is_display
                , `event`.start_date AS start_date
                , `event`.end_date AS end_date 
                , `event`.banner_image AS banner_image
                , `event`.detail_image AS detail_image
            FROM `events` AS `event`
                INNER JOIN event_types AS event_type
                    ON `event`.event_type_id = event_type.id
                INNER JOIN event_kinds AS event_kind
                    ON `event`.event_kind_id = event_kind.id
            WHERE
                `event`.is_deleted = 0
                AND `event`.id = %(event_id)s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            event = cursor.fetchone()
            if not event:
                raise EventDoesNotExist('event does not exist')
            return event

    def get_event_buttons(self, connection, data):
        """ 이벤트가 버튼형일때 버튼 불러오기

        Args:
            connection: 데이터베이스 연결 객체
            data   : 비지니스 레이어에서 넘겨 받은 딕셔너리

        Author: 강두연

        Returns:
            return [
                {
                    "id": 1,
                    "name": "1번 버튼",
                    "order_index": 1,
                    "product_count": 20
                },
                {
                    "id": 2,
                    "name": "2번 버튼",
                    "order_index": 2,
                    "product_count": 20
                },
                {
                    "id": 3,
                    "name": "3번 버튼",
                    "order_index": 3,
                    "product_count": 19
                }
            ]

        History:
            2020-12-30(강두연): 초기 생성
        """

        sql = """
            SELECT
                id
                , (SELECT COUNT(CASE WHEN events_products.event_button_id = event_buttons.id  THEN 1 END)
                    FROM events_products) AS product_count
                , order_index
                , `name`
            FROM
                event_buttons
            WHERE
                is_deleted = 0 
                AND event_id = %(event_id)s
            ORDER BY 
                order_index;   
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            buttons = cursor.fetchall()

            return buttons

    def get_event_products(self, connection, data):
        """ 기획전에 등록된 상품 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 비지니스 레이어에서 넘겨 받은 딕셔너리

        Returns:
            return [
                {
                    "discount_rate": 0.1,
                    "discounted_price": 9000.0,
                    "event_button_id": null, # 이벤트가 버튼형일때는 버튼 아이디가 들어옴
                    "event_id": 1,
                    "id_discount": "할인",
                    "is_display": "진열",
                    "is_sale": "판매",
                    "original_price": 10000.0,
                    "product_created_at": "2020-12-25 00:17:36",
                    "product_id": 40,
                    "product_name": "성보의하루40",
                    "product_number": "P0000000000000000040",
                    "seller_name": "나는셀러6",
                    "thumbnail_image_url": "https://img.freepik.com/free-psd/sample"
                },
                {
                    "discount_rate": 0.1,
                    "discounted_price": 9000.0,
                    "event_button_id": null, # 이벤트가 버튼형일때는 버튼 아이디가 들어옴
                    "event_id": 1,
                    "id_discount": "할인",
                    "is_display": "진열",
                    "is_sale": "판매",
                    "original_price": 10000.0,
                    "product_created_at": "2020-12-25 00:17:36",
                    "product_id": 39,
                    "product_name": "성보의하루39",
                    "product_number": "P0000000000000000039",
                    "seller_name": "나는셀러9",
                    "thumbnail_image_url": "https://img.freepik.com/free-psd/sample"
                }
            ]

            History:
                2020-12-30(강두연): 초기 생성
        """
        sql = """
            SELECT 
                event_product.product_id
                , event_product.event_id
                , event_product.event_button_id
                , product_image.image_url AS thumbnail_image_url
                , product.product_code AS product_number
                , product.`name` AS product_name
                , seller.`name` AS seller_name
                , product.created_at AS product_created_at
                , product.origin_price AS original_price
                , product.discounted_price AS discounted_price
                , CASE WHEN product.is_sale = 0 THEN '미판매' ELSE '판매' END AS is_sale
                , CASE WHEN product.is_display = 0 THEN '미진열' ELSE '진열' END AS is_display
                , CASE WHEN product.discount_rate = 0.00 THEN '미할인' ELSE '할인' END AS id_discount
                , product.discount_rate AS discount_rate
            FROM events_products AS event_product
                INNER JOIN products AS product
                    ON event_product.product_id = product.id
                INNER JOIN product_images AS product_image
                    ON event_product.product_id = product_image.product_id AND product_image.order_index = 1
                INNER JOIN sellers AS seller
                    ON product.seller_id = seller.account_id
            WHERE 
                event_product.event_id = %(event_id)s
                AND event_product.is_deleted = 0
            ORDER BY 
                event_product.id DESC;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            products = cursor.fetchall()

            return products

    def get_event_products_count(self, connection, data):
        """ 기획전에 등록된 상품 갯수 (기획전이 상품형일 때)

        Args:
            connection: 데이터베이스 연결 객체
            data   : 비지니스 레이어에서 넘겨 받은 딕셔너리

        Returns:
            return 40 (int)

        History:
            2020-12-30(강두연): 작성
        """

        sql = """
            SELECT 
                COUNT(*) AS total_count
            FROM 
                events_products
            WHERE
                event_id = %(event_id)s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            count = cursor.fetchone()

            return count['total_count']
