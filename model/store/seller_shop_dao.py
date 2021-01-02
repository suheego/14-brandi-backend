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
            "product_sales_count": null,
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
            "product_sales_count": null,
            "seller_id": 4,
            "seller_name": "나는셀러4"
            }
            ]

        History:
            2021-01-02(고수희): 초기 생성
        """

        sql = """
        SELECT 
            product_image.image_url AS image
            , product.seller_id AS seller_id
            , seller.name AS seller_name
            , product.id AS product_id
            , product.name AS product_name
            , product.origin_price AS origin_price
            , product.discount_rate AS discount_rate
            , product.discounted_price AS discounted_price
            , product_sales_volume.sales_count AS product_sales_count
        FROM 
            products AS product
            INNER JOIN product_images AS product_image
                ON product.id = product_image.product_id AND product_image.order_index = 1
            INNER JOIN sellers AS seller 
                ON seller.account_id = product.seller_id
            LEFT JOIN product_sales_volumes AS product_sales_volume
                ON product_sales_volume.product_id = product.id
        WHERE 
            product.seller_id = %(seller_id)s 
            AND product.name LIKE %(keyword)s
            AND product.is_deleted = 0
        ORDER BY 
            product.id DESC
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

                # 상품 판매량이 없을 경우
                for result in results:
                    if result['product_sales_count'] is None:
                        result['product_sales_count'] = 0

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
            'errorMessage': 'seller_category_not_exist'} : 셀러 카테고리 조회 실패
            400, {'message': 'category does not exist',
            'errorMessage': 'category_not_exist'} : 카테고리 조회 실패

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
                        "product_sales_count": 0,
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
                        "product_sales_count": 0,
                        "seller_id": 4,
                        "seller_name": "나는셀러4"
                    }
                ]

        History:
            2021-01-02(고수희): 초기 생성
        """

        sql = """
        SELECT 
            product_image.image_url AS image
            , product.seller_id AS seller_id
            , seller.name AS seller_name
            , product.id AS product_id
            , product.name AS product_name
            , product.origin_price AS origin_price
            , product.discount_rate AS discount_rate
            , product.discounted_price AS discounted_price
            , product_sales_volume.sales_count AS product_sales_count
        FROM 
            products AS product
            INNER JOIN product_images AS product_image
                ON product.id = product_image.product_id AND product_image.order_index = 1
            INNER JOIN sellers AS seller 
                ON seller.account_id = product.seller_id
            LEFT JOIN product_sales_volumes AS product_sales_volume
                ON product_sales_volume.product_id = product.id
        """

        try:
            # 최신순 정렬일 경우
            if data['type'] == "latest":
                latest_sql = """
                WHERE product.seller_id = %(seller_id)s 
                AND product.is_deleted = 0
                ORDER BY product.id DESC
                LIMIT %(limit)s
                OFFSET %(offset)s
                ;
                """

                sql += latest_sql

            #인기순 정렬일 경우
            else:
                popular_sql = """
                WHERE product.seller_id = %(seller_id)s 
                AND product.is_deleted = 0
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

                # 상품 판매량이 없을 경우
                for result in results:
                    if result['product_sales_count'] is None:
                        result['product_sales_count'] = 0

                return results

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')
