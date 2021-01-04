import traceback
import pymysql

from utils.custom_exceptions import (
    SellerNotExist,
    ServerError,
    SellerCategoryNotExist,
)


class SellerShopDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2021-01-01(고수희): 초기 생성
    """

    def get_seller_info_dao(self, connection, account_id):
        """셀러 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            account_id   : 서비스 레이어에서 넘겨 받아 조회할 account_id

        Author: 고수희

        Returns:
            {
            "background_image": "https://img.freepik.com/free-psd/top-view-t-shirt-concept-mock-up_23-2148809114.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477",
            "english_name": "i am seller_2",
            "id": 2,
            "name": "나는셀러2",
            "profile_image": "https://img.freepik.com/free-psd/logo-mockup-white-paper_1816-82.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477"
            }

        History:
            2021-01-01(고수희): 초기 생성

        Raises:
            400, {'message': 'seller does not exist',
            'errorMessage': 'seller_does_not_exist'} : 셀러 정보 조회 실패
            500, {'message': 'server error',
            'errorMessage': 'server_error'}': 서버 에러
        """

        sql = """
        SELECT 
        account_id AS id
        , name
        , english_name
        , profile_image_url AS profile_image
        , background_image_url AS background_image
        FROM sellers
        WHERE account_id = %s
        AND is_deleted = 0
        ; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, account_id)
                result = cursor.fetchone()
                if not result:
                    raise SellerNotExist('seller_not_exist')
                return result

        except SellerNotExist as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def get_seller_product_search_dao(self, connection, data):
        """셀러 상품 검색 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            [
            {
            "discount_rate": 0.1,
            "discounted_price": 9000.0,
            "image": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
            "origin_price": 10000.0,
            "product_id": 7,
            "product_name": "성보의하루7",
            "seller_id": 4,
            "seller_name": "나는셀러4"
            },
            {
            "discount_rate": 0.1,
            "discounted_price": 9000.0,
            "image": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
            "origin_price": 10000.0,
            "product_id": 5,
            "product_name": "성보의하루5",
            "seller_id": 4,
            "seller_name": "나는셀러4"
            }
            ]

        Raises:
            500, {'message': 'server error',
            'errorMessage': 'server_error'}': 서버 에러

        History:
            2021-01-02(고수희): 초기 생성
        """

        sql = """
        SELECT 
        pi.image_url AS image
        , pd.seller_id AS seller_id
        , se.name AS seller_name
        , pd.id AS product_id
        , pd.name AS product_name
        , pd.origin_price AS origin_price
        , pd.discount_rate AS discount_rate
        , pd.discounted_price AS discounted_price
        FROM products AS pd
        INNER JOIN product_images AS pi ON pi.product_id = pd.id AND pi.order_index = 1
        INNER JOIN sellers AS se ON se.account_id = pd.seller_id
        LEFT JOIN product_sales_volumes AS psv ON psv.product_id = pd.id
        WHERE pd.seller_id = %(seller_id)s 
        AND pd.name LIKE %(keyword)s
        AND pd.is_deleted = 0
        ORDER BY pd.id DESC
        LIMIT %(limit)s
        OFFSET %(offset)s
        ; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                data['keyword'] = "%"+data['keyword']+"%"
                cursor.execute(sql, data)
                results = cursor.fetchall()

                # 상품 검색 결과가 없을 경우
                if not results:
                    return "등록된 상품이 없습니다."
                return results

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def get_seller_category_dao(self, connection, data):
        """셀러 상품 카테고리 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data 

        Author: 고수희

        Returns:
            [
                {
                    "main_category_id": 1,
                    "name": "아우터"
                },
                {
                    "main_category_id": 2,
                    "name": "상의"
                }
            ]
        History:
            2021-01-01(고수희): 초기 생성

        Raises:
            400, {'message': 'seller category does not exist',
            'errormessage': 'seller_category_not_exist'} : 셀러 카테고리 조회 실패
            500, {'message': 'server error',
            'errorMessage': 'server_error'}': 서버 에러
        """

        sql = """
        SELECT DISTINCT 
        pd.main_category_id
        , mc.name
        FROM products as pd
        INNER JOIN main_categories as mc ON mc.id = pd.main_category_id
        WHERE pd.seller_id = %(seller_id)s 
        ; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()

                #셀러 카테고리가 없을 경우
                if not result:
                    raise SellerCategoryNotExist('seller_category_not_exist')
                return result

        except SellerCategoryNotExist as e:
            traceback.print_exc()
            raise e

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def get_seller_product_list_dao(self, connection, data):
        """셀러 상품 리스트 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
             [
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "image": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
                        "origin_price": 10000.0,
                        "product_id": 7,
                        "product_name": "성보의하루7",
                        "seller_id": 4,
                        "seller_name": "나는셀러4"
                    },
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "image": "https://img.freepik.com/free-psd/simple-black-men-s-tee-mockup_53876-57893.jpg?size=338&ext=jpg&ga=GA1.2.1060993109.1605750477",
                        "origin_price": 10000.0,
                        "product_id": 5,
                        "product_name": "성보의하루5",
                        "seller_id": 4,
                        "seller_name": "나는셀러4"
                    }

        Raises:
            500, {'message': 'server error',
            'errorMessage': 'server_error'}': 서버 에러

        History:
            2021-01-02(고수희): 초기 생성
        """

        sql = """
        SELECT 
        pi.image_url AS image
        , pd.seller_id AS seller_id
        , se.name AS seller_name
        , pd.id AS product_id
        , pd.name AS product_name
        , pd.origin_price AS origin_price
        , pd.discount_rate AS discount_rate
        , pd.discounted_price AS discounted_price
        , psv.sales_count AS product_sales_count
        FROM products AS pd
        INNER JOIN product_images AS pi ON pi.product_id = pd.id AND pi.order_index = 1
        INNER JOIN sellers AS se ON se.account_id = pd.seller_id
        LEFT JOIN product_sales_volumes AS psv ON psv.product_id = pd.id
        """

        try:
            #특정 카테고리를 선택한 경우
            if not data['category'] is None:
                category_sql = """
                WHERE pd.main_category_id = %(category)s
                AND pd.seller_id = %(seller_id)s 
                """

                sql += category_sql

            #특정 카테고리를 선택하지 않은 경우
            else:
                all_sql = """
                WHERE pd.seller_id = %(seller_id)s
                """

                sql += all_sql

            # 최신순 정렬일 경우
            if data['type'] == "latest":
                latest_sql = """
                AND pd.is_deleted = 0
                ORDER BY pd.id DESC
                LIMIT %(limit)s
                OFFSET %(offset)s
                ;
                """

                sql += latest_sql

            #인기순 정렬일 경우
            else:
                popular_sql = """
                AND pd.is_deleted = 0
                ORDER BY product_sales_count DESC
                LIMIT %(limit)s
                OFFSET %(offset)s 
                ;
                """

                sql += popular_sql

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                results = cursor.fetchall()

                # 상품 검색 결과가 없을 경우
                if not results:
                    return "등록된 상품이 없습니다."
                return results

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')
