import pymysql

from utils.custom_exceptions import DatabaseError


class ProductListDao:

    def get_search_products_dao(self, connection, search):

        sql = """
        SELECT 
	    name
        FROM
            products
        WHERE
            name
        LIKE %s;
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            search_string = "'%"+search+"%'"
            cursor.execute(sql, search_string)
            result = cursor.fetchall()
            print(result)
            return result

    def get_product_list(self, connection, data):
        """ 상품 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                product_list : 30개 단위

            Raises:
                500, {'message': 'database_error', 'errorMessage': format(e)} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성

            Notes:
                현재 데이터에서 이미지가 없는 상품들이 있기 때문에 INNER JOIN이 아닌 LEFT JOIN을 사용
                상품 판매 수량 테이블은 상품이 만들어질 때 생성되는 게 아닌 처음 판매가 되는 시점에서 생기는 테이블이기 때문에 LEFT JOIN을 사용
        """

        sql = """
        SELECT 
            product_image.image_url AS image
            , product.seller_id AS seller_id
            , seller.`name` AS seller_name
            , product.id AS product_id
            , product.`name` AS product_name
            , product.origin_price
            , product.discount_rate
            , product.discounted_price 
            , product_sales_volume.sales_count
        FROM 
            products AS product
        LEFT JOIN product_images AS product_image 
            ON product.id = product_image.product_id AND product_image.order_index = 1
        INNER JOIN sellers AS seller 
            ON seller.account_id = product.seller_id
        INNER JOIN product_sales_volumes AS product_sales_volume
            ON product_sales_volume.product_id = product.id
        WHERE 
            product.is_deleted = 0
        ORDER BY 
            product.id DESC
        LIMIT %(offset)s, %(limit)s; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception as e:
            raise DatabaseError(format(e))

    def get_event_list(self, connection, data):
        """ 상품 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스에서 넘겨 받은 dict 객체

            Author: 김민구

            Returns:
                event_list : 1개 혹은 2개

            Raises:
                500, {'message': 'database_error', 'errorMessage': format(e)} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
        """

        sql = """
            SELECT 
                id
                , banner_image
            FROM 
                events
            WHERE 
                end_date > now()
                AND is_display = 1
                AND is_deleted = 0
            ORDER BY 
                id DESC
            LIMIT %(offset)s, %(limit)s; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception as e:
            raise DatabaseError(format(e))

    def get_first_category_list(self, connection):
        """ menu 카테고리 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                result (menus)

            Raises:
                500, {'message': 'database_error', 'errorMessage': format(e)} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
        """

        sql = """
            SELECT 
                id
                , `name` 
            FROM 
                menus
            WHERE
                is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

        except Exception as e:
            raise DatabaseError(format(e))

    def get_second_category_list(self, connection):
        """ main 카테고리 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                result (main_categories)

            Raises:
                500, {'message': 'database_error', 'errorMessage': format(e)} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
        """

        sql = """
            SELECT 
                id 
                , `name`
                , menu_id 
            FROM 
                main_categories
            WHERE     
                is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

        except Exception as e:
            raise DatabaseError(format(e))

    def get_third_category_list(self, connection):
        """ sub 카테고리 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                result (sub_categories)

            Raises:
                500, {'message': 'database_error', 'errorMessage': format(e)} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
        """

        sql = """
            SELECT 
                id
                , `name`
                , main_category_id 
            FROM 
                sub_categories
            WHERE
                is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

        except Exception as e:
            raise DatabaseError(format(e))
