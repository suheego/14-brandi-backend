import traceback

import pymysql

from utils.custom_exceptions import DatabaseError


class ProductListDao:
    """ Persistence Layer

        Attributes: None

        Author: 김민구

        History:
            2020-12-30(김민구): 초기 생성
            2020-12-31(김민구): 에러 문구 변경
    """

    def get_search_products_dao(self, connection, data):
        """ 상품 검색 및 정렬

            검색키워드로 상품이름과 셀러이름을 검색하고
            검색 결과를 추천순, 판매순, 최신순으로 정렬한다.

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 data

            Author: 김기용
            
            Returns: {
                        "bookmark_count": 0,
                        "discounted_price": 9000.0,
                        "image": "https://img.freepik.com",
                        "name": "성보의하루999",
                        "origin_price": 10000.0,
                        "product_id": 999,
                        "sales_count": 32,
                        "seller_id": 4,
                        "seller_name": "나는셀러4"
                        }

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-31(김기용): 초기 생성
                2021-01-01(김기용): 1차 수정: 정렬기능추가
                2021-01-02(김기용): 2차 수정: 북마크 정렬기능 추가
        """

        sql = """
        SELECT DISTINCT
            product_image.image_url AS image
            , product.name AS product_name
            , product.seller_id AS seller_id
            , seller.name AS seller_name
            , product.id AS product_id
            , product.origin_price
            , product.discounted_price
            , product_sales_volume.sales_count
            , bookmark.bookmark_count
        FROM
            products AS product
        INNER JOIN product_images AS product_image
            ON product_id = product_image.product_id
            AND product_image.order_index = 1
        INNER JOIN sellers AS seller
            ON seller.account_id = product.seller_id
        INNER JOIN product_sales_volumes AS product_sales_volume
            ON product_sales_volume.product_id = product.id
        INNER JOIN bookmark_volumes AS bookmark
            ON bookmark.product_id = product.id
        WHERE
            product.name LIKE %(search)s
            AND product.is_deleted=0
        ORDER BY
             (CASE WHEN %(sort_type)s=1 THEN bookmark_count END) DESC
            , (CASE WHEN %(sort_type)s=2 THEN sales_count END) DESC
            , (CASE WHEN %(sort_type)s=3 THEN product.id END) DESC
        LIMIT %(limit)s;

        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                data['search'] = '%%' + data['search'] + '%%' 
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result
        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_product_list(self, connection, event_id):

        """ 상품 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                event_id   : 서비스에서 넘겨 받은 int

            Author: 김민구

            Returns: 30개의 상품정보
                [
                    {
                        'image': 'url',
                        'seller_id': 1,
                        'seller_name': '둘리',
                        'product_id': 1,
                        'product_name': '성보의 하루',
                        'origin_price': 10000.0,
                        'discount_rate': 0.1,
                        'discounted_price': 9000.0,
                        'sales_count': 30
                    },
                ]

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경 / 이벤트에 대한 상품을 반환하는 작업으로 수정
        """

        sql = """
            SELECT 
                product_image.image_url
                , product.seller_id AS seller_id
                , seller.`name` AS seller_name
                , product.id AS product_id
                , product.`name` AS product_name
                , product.origin_price
                , product.discount_rate
                , product.discounted_price 
                , product_sales_volume.sales_count
            FROM
            events_products AS event_product
            INNER JOIN products AS product
                ON event_product.product_id = product.id
            INNER JOIN product_images AS product_image
                ON product_image.product_id = product.id
            INNER JOIN sellers AS seller
                ON seller.account_id = product.seller_id
            INNER JOIN product_sales_volumes AS product_sales_volume
                ON product_sales_volume.product_id = product.id
            WHERE
                event_id = %s
                AND product.is_deleted = 0
                AND product.is_display = 1
            ORDER BY
                product.id DESC
            LIMIT 30;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, event_id)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event(self, connection, offset):
        """ 상품 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                offset     : 서비스에서 넘겨 받은 int

            Author: 김민구

            Returns:
                {
                    event_id: 1,
                    event_banner_image: 'url'
                }

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경 / 1개의 이벤트 배너 반환하는 작업으로 수정
        """

        sql = """
            SELECT 
                id AS event_id
                , banner_image AS event_banner_image
            FROM 
                events
            WHERE 
                end_date > now()
                AND is_display = 1
                AND is_deleted = 0
            ORDER BY 
                id ASC
            LIMIT %s, 1
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, offset)
                result = cursor.fetchone()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_product_image_dao(self, connection, data):
        """ 상품 이미지들을 조회한다.

            Args:
                connection : 데이터베이스 연결 객체
                offset     : 서비스에서 넘겨 받은 int

            Author: 김기용

            Returns:
                {
                    image_id: 1,
                    images_url: www.example.com
                }

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-01-00(김기용): 초기 생성
        """

        sql = """
        SELECT DISTINCT
            product_image.id AS image_id
            , product_image.image_url AS image_url
        FROM
            product_images AS product_image
        WHERE
            product_id = %(product_id)s

        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                images = cursor.fetchall()
                return images 

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_product_color_dao(self, connection, data):
        """ 상품 컬러들을 조회한다.

            상품이 여러 컬러들을 가질 수 있게 되고
            컬러도 여러 상품들을 가질 수 있게 됨으로
            중복이 발생한다. 그래서 DISTINCT를 사용

            Args:
                connection : 데이터베이스 연결 객체
                data     : 서비스에서 넘겨 받은 data

            Author: 김기용

            Returns:
                {
                    color_id: 1,
                    color_name: black
                }

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-01-00(김기용): 초기 생성
        """

        sql = """
            SELECT DISTINCT
                color.name AS color_name
                , color.id AS color_id
            FROM
                stocks
            INNER JOIN colors as color
                ON stocks.color_id = color.id
            WHERE product_id = %(product_id)s
            ;
        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                color = cursor.fetchall()
                return color

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_product_size_dao(self, connection, data):
        """ 상품 사이즈를 조회한다.

            상품이 여러 사이즈들을 가질 수 있게 되고
            사이즈도 여러 상품들을 가질 수 있게 됨으로
            중복이 발생한다. 그래서 DISTINCT 를 사용

            Args:
                connection : 데이터베이스 연결 객체
                data     : 서비스에서 넘겨 받은 data

            Author: 김기용

            Returns:
                {
                    size_id: 1,
                    size_name: black
                }

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}

            History:
                2020-01-00(김기용): 초기 생성
        """
        
        sql = """
            SELECT DISTINCT
                size.id AS size_id
                ,size.name AS size_name
            FROM
                stocks
            INNER JOIN sizes as size
                ON stocks.size_id = size.id
            WHERE product_id = %(product_id)s
            ;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                sizes = cursor.fetchall()
                return sizes

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_product_detail_dao(self, connection, data):
        """ 상품 상세정보

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 data

            Author: 김기용
            
            Returns: 
                {
                "bookmark_count": 0,
                "detail_information": "html====================",
                "discount_rate": 0.1,
                "discounted_price": 9000.0,
                "id": 1,
                "name": "성보의하루1",
                "origin_price": 10000.0,
                "sales_count": 40,
                "seller_id": 7,
                "seller_name": "나는셀러7"
                }

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-31(김기용): 초기 생성
                2021-01-01(김기용): 1차 수정: 구현 완료
                2021-01-02(김기용): 2차 수정: 북마크 개수 추가
                2021-01-03(김기용): 3차 수정: 유저별 북마크 확인기능 추가
                2021-01-05(김기용): 4차 수정: 비회원 로그인 북마크 반환값 추가
        """

        sql = """
            SELECT 
                product.id AS product_id
                , product.name AS product_name
                , product.detail_information
                , product.seller_id AS seller_id
                , seller.name AS seller_name
                , product.origin_price
                , product.discount_rate
                , product.discounted_price
                , product_sales_volume.sales_count
                , bookmark.bookmark_count
                                        
        """

        sql_with_account = """
                , EXISTS(
                            SELECT
                                id
                            FROM
                                bookmarks
                            WHERE
                                account_id = %(account_id)s
                                AND product_id= %(product_id)s
                                AND is_deleted =0
                            ) AS is_bookmarked
                """

        sql_without_account = """
                    FROM
                        products AS product
                    INNER JOIN stocks AS stock
                        ON stock.product_id = product.id
                    INNER JOIN sellers AS seller
                        ON product.seller_id = seller.account_id
                    INNER JOIN product_sales_volumes AS product_sales_volume
                        ON product_sales_volume.product_id = product.id
                    INNER JOIN bookmark_volumes AS bookmark
                        ON bookmark.product_id = product.id
                    WHERE
                        product.id = %(product_id)s
                        AND product.is_deleted = 0
                        ;
        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                if 'account_id' not in data:
                    sql += sql_without_account
                    cursor.execute(sql, data)
                    result = cursor.fetchone()
                    result['is_bookmarked'] = 0
                    return result
                query = sql + sql_with_account + sql_without_account
                cursor.execute(query, data)
                result = cursor.fetchone()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

