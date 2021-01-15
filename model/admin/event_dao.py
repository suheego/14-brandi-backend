import pymysql
from utils.custom_exceptions import (
    EventDoesNotExist,
    CategoryMenuDoesNotMatch,
    CategoryDoesNotExist,
    CreateEventDenied,
    CreateButtunDenied,
    InsertProductIntoButtonDenied,
    InsertProductIntoEventDenied
)

class EventDao:
    """ Persistence Layer

        Attributes: None

        Author: 강두연

        History:
            2020-12-28(강두연): 초기 생성 및 조회 기능 작성
            2020-12-29(강두연): 이벤트 검색조건별 조회 작성
            2020-12-30(강두연): 이벤트 상세정보 및 수정페이지 기능 작성
            2021-01-02(강두연): 기획전 추가 기능 작성
            2021-01-04(강두연): 기획전 수정 관련기능 작성
            2021-01-05(강두연): 기획전 수정 관련기능 추가, 기획전 관련 INSERT 메소드에서 논리삭제 복구 기능 추가
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
                404, {'message': 'event not exist',
                      'errorMessage': 'event does not exist'} : 이벤트 정보 조회 실패
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

            Raises:
                404, {'message': 'event not exist',
                      'errorMessage': 'event does not exist'} : 이벤트 정보 조회 실패
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
                    "is_discount": "할인",
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
                , CASE WHEN product.discount_rate = 0.00 THEN '미할인' ELSE '할인' END AS is_discount
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
                event_id = %(event_id)s
                AND is_deleted = 0;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            count = cursor.fetchone()

            return count['total_count']

    def get_products_list_to_post(self, connection, data):
        """ 기획전에 추가할 상품 조회

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns: {
                "products": [
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "id": 99,
                        "is_display": 1,
                        "is_sale": 1,
                        "original_price": 10000.0,
                        "product.discounted_price": 9000.0,
                        "product_name": "성보의하루99",
                        "product_number": "P0000000000000000099",
                        "seller_name": "나는셀러5",
                        "thumbnail_image_url": "https://img.com/asdf"
                    },
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "id": 98,
                        "is_display": 1,
                        "is_sale": 1,
                        "original_price": 10000.0,
                        "product.discounted_price": 9000.0,
                        "product_name": "성보의하루98",
                        "product_number": "P0000000000000000098",
                        "seller_name": "나는셀러5",
                        "thumbnail_image_url": "https://img.com/asdf"
                    }
                ],
                "total_count": 31
            }

            History:
                    2020-12-31(강두연): 초기 작성
        """
        total_count_sql = """
            SELECT
                COUNT(*) AS total_count
        """

        sql = """
            SELECT
                product.id
                , product.origin_price AS original_price
                , product.discounted_price AS discounted_price
                , product_image.image_url AS thumbnail_image_url
                , product.product_code AS product_number
                , product.`name` AS product_name
                , seller.`name` AS seller_name
                , product.discounted_price AS discounted_price
                , product.discount_rate AS discount_rate
                , product.is_sale AS is_sale
                , product.is_display AS is_display
        """
        extra_sql = """
            FROM 
                products AS product
                INNER JOIN product_images AS product_image
                    ON product.id = product_image.product_id AND product_image.order_index = 1
                INNER JOIN sellers AS seller
                    ON product.seller_id = seller.account_id
            WHERE 
                product.is_deleted = 0
        """

        # 상품명, 상품번호
        if data['product_name']:
            extra_sql += ' AND product.name LIKE %(product_name)s'
        elif data['product_number']:
            extra_sql += ' AND product.product_code = %(product_number)s'

        # 셀러명, 셀러번호
        if data['seller_name']:
            extra_sql += ' AND seller.`name` = %(seller_name)s'
        elif data['seller_number']:
            extra_sql += ' AND seller.account_id = %(seller_number)s'

        # 상품 등록일
        if data['start_date'] and data['end_date']:
            extra_sql += """
                AND product.created_at BETWEEN CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """

        # 상품분류 -- 구분파트 트랜드, 브랜드, 뷰티 순서
        if data['menu_id'] == 4:
            extra_sql += ' AND seller.seller_attribute_type_id IN (1, 2, 3)'
        elif data['menu_id'] == 5:
            extra_sql += ' AND seller.seller_attribute_type_id IN (4, 5, 6)'
        elif data['menu_id'] == 6:
            extra_sql += ' AND seller.seller_attribute_type_id = 7'

        # 1차 카테고리
        if data['main_category_id']:
            extra_sql += ' AND product.main_category_id = %(main_category_id)s'

        # 2차 카테고리
        if data['sub_category_id']:
            extra_sql += ' AND product.sub_category_id = %(sub_category_id)s'

        sql += extra_sql
        total_count_sql += extra_sql

        sql += ' ORDER BY product.id DESC LIMIT %(page)s, %(length)s;'

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            products = cursor.fetchall()
            if not products:
                return {'products': [], 'total_count': 0}
            cursor.execute(total_count_sql, data)
            count = cursor.fetchone()
            return {'products': products, 'total_count': count['total_count']}

    def get_product_category(self, connection, data):
        """  기획전에 추가될 상품 조회 검색조건에서 카테고리 불러오기

        Args:
            connection: 데이터베이스 연결 객체
            data : 비지니스 레이어에서 넘겨 받은 딕셔너리

        Returns:
            case 1: [
                {
                    "id": 4,
                    "name": "트렌드"
                },
                {
                    "id": 5,
                    "name": "브랜드"
                },
                {
                    "id": 6,
                    "name": "뷰티"
                }
            ]
            case 2: [
                {
                    "id": 1,
                    "name": "아우터"
                },
                {
                    "id": 2,
                    "name": "상의"
                },
                {
                    "id": 3,
                    "name": "바지"
                },
                {
                    "id": 4,
                    "name": "원피스"
                },
                {
                    "id": 5,
                    "name": "스커트"
                },
                {
                    "id": 6,
                    "name": "신발"
                },
                {
                    "id": 7,
                    "name": "가방"
                },
                {
                    "id": 8,
                    "name": "주얼리"
                },
                {
                    "id": 9,
                    "name": "잡화"
                },
                {
                    "id": 10,
                    "name": "라이프웨어"
                },
                {
                    "id": 11,
                    "name": "빅사이즈"
                }
            ]
            case 3: [
                {
                    "id": 1,
                    "name": "자켓"
                },
                {
                    "id": 2,
                    "name": "가디건"
                },
                {
                    "id": 3,
                    "name": "코트"
                },
                {
                    "id": 4,
                    "name": "점퍼"
                },
                {
                    "id": 5,
                    "name": "패딩"
                },
                {
                    "id": 6,
                    "name": "무스탕/퍼"
                },
                {
                    "id": 7,
                    "name": "기타"
                }
            ]
        History:
            2020-12-31(강두연): 초기 작성

        Raises:
            400, {'message': 'menu id does not match with category id',
                  'errorMessage': 'category and menu does not match'}: 카테고리와 메뉴가 매칭안됨

            400, {'message': 'category not exist',
                  'errorMessage': 'category does not exist'}: 카테고리가 존재하지 않음
       """
        if not data['menu_id'] and not data['first_category_id']:
            sql = """
                SELECT
                     id
                     , CASE WHEN id=4 THEN '트렌드' ELSE `name` END AS `name` 
                 FROM 
                    menus WHERE id = 4 OR id = 5 OR id = 6;
            """
        elif data['menu_id'] and not data['first_category_id']:
            sql = """
                SELECT 
                    id
                    , `name` 
                FROM 
                    main_categories 
                WHERE 
                    menu_id = %(menu_id)s;
            """
        elif data['menu_id'] and data['first_category_id']:
            validate_sql = """
                SELECT
                    id
                FROM
                    main_categories
                WHERE
                    menu_id = %(menu_id)s
                AND id = %(first_category_id)s;
            """

            sql = """
                SELECT
                    id
                    , `name`
                FROM
                    sub_categories
                WHERE
                    main_category_id = %(first_category_id)s;
            """
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(validate_sql, data)
                result = cursor.fetchone()
                if not result:
                    raise CategoryMenuDoesNotMatch('category and menu does not match')

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if not result:
                raise CategoryDoesNotExist('category does not exist')
            return result

    def create_event(self, connection, data):
        """ 기획전 생성

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                return 27 (생성된 기획전 프라이머리키 아이디)

            History:
                2021-01-02(강두연): 초기 작성

            Raises:
                400, {'message': 'unable to create event',
                      'errorMessage': 'unable to create event'} : 이벤트 생성 실패
        """
        sql = """
            INSERT INTO `events` (
                `name`
                , start_date
                , end_date
                , banner_image
                , detail_image
                , event_type_id
                , event_kind_id
                , is_display)
            VALUES (
                %(name)s
                , %(start_datetime)s
                , %(end_datetime)s
                , %(banner_image)s
                , %(detail_image)s
                , %(event_type_id)s
                , %(event_kind_id)s
                , %(is_display)s);
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise CreateEventDenied('unable to create event')
            return result

    def create_or_update_button(self, connection, data):
        """ 기획전 버튼 생성

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                return 27 (생성된 버튼 프라이머리키 아이디)

            History:
                2021-01-02(강두연): 초기 작성
                2021-01-04(강두연): 논리 삭제된 버튼과 동일한 이름과 이벤트 아이디의 버튼을 만드려고하면 로우를 생성하지않고 논리삭제 값을 바꿔주게 수정
                2021-01-05(강두연): 사용중인 버튼중에 이름이 같은 버튼이 이미 존재하면 에러 반환

            Raises:
                400, {'message': 'unable to create button',
                      'errorMessage': 'unable to create button'} : 버튼 생성 실패

                400, {'message': 'unable to create button',
                      'errorMessage': 'button name must be unique in an event'} : 버튼 이름 중복
        """
        check_sql = """
            SELECT
                id
            FROM 
                event_buttons
            WHERE
                `name` = %(button_name)s
                AND is_deleted = 1
                AND event_id = %(event_id)s;
        """

        duplicate_check_sql = """
            SELECT
                EXISTS (
                    SELECT
                        *
                    FROM
                        event_buttons
                    WHERE
                        `name` = %(button_name)s
                        AND is_deleted = 0
                        AND event_id = %(event_id)s
                ) AS duplicate_button;
        """

        sql = """
            INSERT INTO event_buttons (
                `name`
                , order_index
                , event_id) 
            VALUES (
                %(button_name)s
                , %(button_index)s
                , %(event_id)s)
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(duplicate_check_sql, data)
            duplicate_check = cursor.fetchone()
            if duplicate_check['duplicate_button']:
                raise CreateButtunDenied('button name must be unique in an event')

            cursor.execute(check_sql, data)
            check = cursor.fetchone()
            if check:
                check['button_index'] = data['button_index']
                sql = """
                    UPDATE
                        event_buttons
                    SET
                        is_deleted = 0
                        order_index = %(button_index)s
                    WHERE id = %(id)s
                """
                cursor.execute(sql, check)
                return check['id']

            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise CreateButtunDenied('unable to create button')
            return result

    def insert_product_into_button(self, connection, data):
        """ 기획전 버튼에 상품 연결

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                return 27 (연결된 기획전 상품 프라이머리키 아이디)

            History:
                2021-01-02(강두연): 초기 작성

            Raises:
                400, {'message': 'unable to insert product into button',
                      'errorMessage': 'unable to insert product into button'} : 상품 연결 실패
        """

        check_sql = """
            SELECT
                id
            FROM
                events_products
            WHERE
                event_id = %(event_id)s
                AND product_id = %(product_id)s
                AND event_button_id = %(button_id)s
                AND is_deleted = 1;
        """

        duplicate_check_sql = """
            SELECT
                EXISTS (
                    SELECT
                        *
                    FROM
                        events_products
                    WHERE
                        event_id = %(event_id)s
                        AND product_id = %(product_id)s
                        AND is_deleted = 0
                ) AS duplicate_event_product;
        """

        sql = """
            INSERT INTO events_products (
                event_id
                , product_id
                , event_button_id) 
            VALUES (
                %(event_id)s
                , %(product_id)s
                , %(button_id)s);
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(duplicate_check_sql, data)
            duplicate_check = cursor.fetchone()
            if duplicate_check['duplicate_event_product']:
                raise InsertProductIntoButtonDenied('product is already included')
            cursor.execute(check_sql, data)
            check = cursor.fetchone()
            if check:
                cursor.execute("""
                    UPDATE
                        events_products
                    SET
                        is_deleted = 0
                    WHERE
                        id = %(id)s
                """, check)
                return
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise InsertProductIntoButtonDenied('unable to insert product into button')
            return result

    def insert_product_into_event(self, connection, data):
        """ 기획전에 상품 연결 (버튼형 x)

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                return 27 (연결된 기획전 상품 프라이머리키 아이디)

            History:
                2021-01-02(강두연): 초기 작성
                2021-01-04(강두연): 논리삭제된 같은 기획전, 상품 아이디를 가진 로우가 있을경우 복구 작성
                2021-01-05(강두연): 같은 기획전 내에 중복상품있는지 체크 추가

            Raises:
                400, {'message': 'unable to insert product into event',
                      'errorMessage': 'unable to insert product into event'} : 상품 연결 실패
        """
        check_sql = """
            SELECT
                id
            FROM
                events_products
            WHERE
                event_id = %(event_id)s
                AND product_id = %(product_id)s
                AND is_deleted = 1;
        """

        duplicate_check_sql = """
            SELECT
                EXISTS (
                    SELECT
                        *
                    FROM
                        events_products
                    WHERE
                        event_id = %(event_id)s
                        AND product_id = %(product_id)s
                        AND is_deleted = 0
                ) AS duplicate_event_product;
        """

        sql = """
            INSERT INTO events_products (
                event_id
                , product_id) 
            VALUES (
                %(event_id)s
                , %(product_id)s);
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(duplicate_check_sql, data)
            duplicate_check = cursor.fetchone()
            if duplicate_check['duplicate_event_product']:
                raise InsertProductIntoEventDenied('product is already included')
            cursor.execute(check_sql, data)
            check = cursor.fetchone()
            if check:
                cursor.execute("""
                    UPDATE
                        events_products
                    SET
                        is_deleted = 0
                    WHERE
                        id = %(id)s
                """, check)
                return
            cursor.execute(sql, data)
            result = cursor.lastrowid
            if not result:
                raise InsertProductIntoEventDenied('unable to insert product into event')
            return result

    def delete_buttons_by_event(self, connection, data):
        """ 이벤트 아이디로 버튼 삭제

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                None

            History:
                2021-01-04(강두연): 작성
        """
        sql = """
            UPDATE 
                event_buttons
            SET 
                is_deleted = 1
            WHERE
                event_id = %(event_id)s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)

    def delete_event_products_by_event(self, connection, data):
        """ 이벤트 아이디로 기획전 상품 삭제

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                None

            History:
                2021-01-04(강두연): 작성
        """
        sql = """
            UPDATE
                events_products
            SET
                is_deleted = 1
            WHERE
                event_id = %(event_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)

    def delete_event(self, connection, data):
        """ 기획전 아이디로 기획전 삭제

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                None

            History:
                2021-01-04(강두연): 작성
        """
        sql = """
            UPDATE 
                `events`
            SET
               is_deleted = 1
            WHERE
                id = %(event_id)s 
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)

    def update_event_detail(self, connection, data):
        """ 기획전 상세정보 업데이트

            Args:
                connection: 데이터베이스 연결 객체
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                None

            History:
                2021-01-04(강두연): 작성
        """

        sql = """
            UPDATE 
                `events`
            SET
                `name` = %(name)s
                , start_date = %(start_datetime)s
                , end_date = %(end_datetime)s
                , is_display = %(is_display)s
        """

        if data['banner_image_uploaded']:
            sql += ', banner_image = %(banner_image)s'

        if data['detail_image_uploaded']:
            sql += ', detail_image = %(detail_image)s'

        sql += 'WHERE id = %(event_id)s;'

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)

    def get_event_kind_id(self, connection, event_id):
        """ 기획전 아이디로 기획전 종류 아이디 받기 (버튼형, 상품형)

            Args:
                connection: 데이터베이스 연결 객체
                event_id : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Returns:
                1 or 2

            History:
                2021-01-04(강두연): 작성
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    event_kind_id
                FROM 
                    `events`
                WHERE id = %s;
            """, event_id)
            event_kind = cursor.fetchone()

            return event_kind['event_kind_id']

    def update_event_button(self, connection, button):
        """ 버튼에 관한 정보 수정

            Args:
                connection: 데이터베이스 연결 객체
                button : 비지니스 레이어에서 넘겨 받은 버튼에대한 정보를 담고있는 딕셔너리

            Returns:
                None

            History:
                2021-01-05(강두연): 작성
                2021-01-06(강두연): 미사용
        """

        sql = """
            UPDATE 
                event_buttons
            SET
                `name` = %(button_name)s
                , order_index = %(button_index)s
            WHERE
                event_id = %(event_id)s
                AND id = %(id)s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, button)

    def delete_event_button(self, connection, button):
        """ 기획전 버튼 논리삭제

            Args:
                connection: 데이터베이스 연결 객체
                button : 비지니스 레이어에서 넘겨 받은 버튼에대한 정보를 담고있는 딕셔너리

            Returns:
                None

            History:
                2021-01-05(강두연): 작성
        """

        sql = """
            UPDATE
                event_buttons
            SET
                is_deleted = 1
            WHERE
                id = %s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, button)

    def move_button_products(self, connection, product):
        """ 버튼형 기획전 상품 종속 버튼 변경

            Args:
                connection: 데이터베이스 연결 객체
                product : 비지니스 레이어에서 넘겨 받은 상품에대한 정보를 담고있는 딕셔너리

            Returns:
                None

            History:
                2021-01-05(강두연): 작성
        """

        sql = """
            UPDATE
                events_products
            SET
                event_button_id = %(button_id)s
            WHERE
                event_id = %(event_id)s
                AND product_id = %(product_id)s
                AND is_deleted = 0;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, product)

    def delete_event_product(self, connection, product):
        """ 기획전 상품 논리삭제

            Args:
                connection: 데이터베이스 연결 객체
                product : 비지니스 레이어에서 넘겨 받은 상품에대한 정보를 담고있는 딕셔너리

            Returns:
                None

            History:
                2021-01-05(강두연): 작성
        """
        sql = """
            UPDATE
                events_products
            SET
                is_deleted = 1
            WHERE
                product_id = %(product_id)s
                AND event_id = %(event_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, product)
