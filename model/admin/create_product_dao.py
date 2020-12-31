import pymysql

from utils.custom_exceptions import (
    ProductCreateDenied,
    ProductCodeUpdatedDenied,
    ProductImageCreateDenied,
    StockCreateDenied,
    ProductHistoryCreateDenied,
    ProductSalesVolume,
    ProductOriginTypesNotExist,
    ColorNotExist,
    SizeNotExist,
    MainCategoryNotExist,
    SubCategoryNotExist
)

class CreateProductDao:
    """ Persistence Layer

        Attributes: None

        Author: 심원두

        History:
            2020-12-29(심원두): 초기 생성
    """

    def insert_product(self, connection, data):
        """상품 정보 등록 (상품 정보 테이블)

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받은 상품등록에 사용될 데이터

        Author: 심원두

        Returns:
            return product_id # products 테이블에 신규 등록된 데이터의 pk (id) 값

        History:
            2020-12-29(심원두): 초기 생성

        Raises:
            500, {'message': 'product create denied', 'errorMessage': 'unable_to_create_product'}
            : 상품 정보 등록 실패
        """

        sql = """
            INSERT INTO products (
                `is_display`
                ,`is_sale`
                ,`main_category_id`
                ,`sub_category_id`
                ,`is_product_notice`
                ,`manufacturer`
                ,`manufacturing_date`
                ,`product_origin_type_id`
                ,`name`
                ,`description`
                ,`detail_information`
                ,`origin_price`
                ,`discount_rate`
                ,`discounted_price`
                ,`discount_start_date`
                ,`discount_end_date`
                ,`minimum_quantity`
                ,`maximum_quantity`
                ,`seller_id`
                ,`account_id`
            ) VALUES (
                %(is_display)s
                ,%(is_sale)s
                ,%(main_category_id)s
                ,%(sub_category_id)s
                ,%(is_product_notice)s
                ,%(manufacturer)s
                ,%(manufacturing_date)s
                ,%(product_origin_type_id)s
                ,%(product_name)s
                ,%(description)s
                ,%(detail_information)s
                ,%(origin_price)s
                ,%(discount_rate)s
                ,%(discounted_price)s
                ,%(discount_start_date)s
                ,%(discount_end_date)s
                ,%(minimum_quantity)s
                ,%(maximum_quantity)s
                ,%(seller_id)s
                ,%(account_id)s
            );
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            product_id = cursor.lastrowid

            if not product_id:
                raise ProductCreateDenied('unable_to_create_product')

            return product_id

    def update_product_code(self, connection, data):
        """상품 정보 갱신

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 정보 갱신에 사용될 데이터

            Author: 심원두

            Returns:
                return None

            History:
                2020-12-29(심원두): 초기 생성

            Raises:
                500, {'message': 'product code update denied', 'errorMessage': 'unable_to_update_product_code'}
                : 상품 코드 갱신 실패
        """

        sql = """
            UPDATE
                products
            SET
                `product_code` = %(product_code)s
            WHERE
                id = %(product_id)s
            AND
                is_deleted = 0;
        """

        with connection.cursor() as cursor:
            result = cursor.execute(sql, data)

            if not result:
                raise ProductCodeUpdatedDenied('unable_to_update_product_code')

    def insert_product_image(self, connection, data):
        """상품 이미지 정보 등록

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 이미지 등록에 사용될 데이터

            Author: 심원두

            Returns:
                return None

            History:
                2020-12-29(심원두): 초기 생성

            Raises:
                500, {'message': 'product image create denied', 'errorMessage': 'unable_to_create_product_image'}
                : 상품 이미지 정보 등록 실패
        """

        sql = """
            INSERT INTO product_images(
                `image_url`
                , `product_id`
                , `order_index`
            ) VALUES (
                %(image_url)s
                ,%(product_id)s
                ,%(order_index)s
            );
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid

            if not result:
                raise ProductImageCreateDenied('unable_to_create_product_image')

    def insert_stock(self, connection, data):
        """상품 옵션 정보 등록

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 옵션 정보 이미지 등록에 사용될 데이터

            Author: 심원두

            Returns:
                return None

            History:
                2020-12-29(심원두): 초기 생성

            Raises:
                500, {'message': 'stock create denied', 'errorMessage': 'unable_to_create_stocks'}
                : 상품 이미지 정보 등록 실패
        """

        sql = """
            INSERT INTO stocks(
                 `product_option_code`
                , `remain`
                , `color_id`
                , `size_id`
                , `product_id`
            ) VALUES (
                %(product_option_code)s
                ,%(remain)s
                ,%(color_id)s
                ,%(size_id)s
                ,%(product_id)s
            );
        """

        with connection.cursor() as cursor:
            result = cursor.execute(sql, data)

            if not result:
                raise StockCreateDenied('unable_to_create_stocks')

    def insert_product_history(self, connection, data):
        """상품 이력 정보 등록

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 옵션 정보 이미지 등록에 사용될 데이터

            Author: 심원두

            Returns:
                return None

            History:
                2020-12-29(심원두): 초기 생성

            Raises:
                500, {'message': 'product history create denied', 'errorMessage': 'unable_to_create_product_history'}
                : 상품 이미지 정보 등록 실패
        """

        sql = """
            INSERT INTO product_histories (
                `product_id`
                ,`product_name`
                ,`is_display`
                ,`is_sale`
                ,`origin_price`
                ,`discounted_price`
                ,`discount_rate`
                ,`discount_start_date`
                ,`discount_end_date`
                ,`minimum_quantity`
                ,`maximum_quantity`
                ,`updater_id`
                ,`is_product_deleted`
            ) VALUES (
                %(product_id)s
                ,%(product_name)s
                ,%(is_display)s
                ,%(is_sale)s
                ,%(origin_price)s
                ,%(discounted_price)s
                ,%(discount_rate)s
                ,%(discount_start_date)s
                ,%(discount_end_date)s
                ,%(minimum_quantity)s
                ,%(maximum_quantity)s
                ,%(account_id)s
                ,%(is_product_deleted)s
            );
        """

        with connection.cursor() as cursor:
            result = cursor.execute(sql, data)

            if not result:
                raise ProductSalesVolume('unable_to_create_product_history')

    def insert_product_sales_volumes(self, connection, product_id):
        sql = """
            INSERT INTO product_sales_volumes (
                `product_id`
            ) VALUES (
                %s
            );
        """
        with connection.cursor() as cursor:
            result = cursor.execute(sql, product_id)

            if not result:
                raise ProductHistoryCreateDenied('unable_to_create_product_sales_volumes')

    def get_product_origin_types(self, connection):
        sql = """
            SELECT
                id
                ,name
            FROM
                product_origin_types
            ;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

            if not result:
                raise ProductOriginTypesNotExist('fail_to_get_product_origin_types')

            return result

    def get_size_list(self, connection):
        """사이즈 정보 취득
            Args:
                connection: 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                return None

            History:
                2020-12-30(심원두): 초기 생성

            Raises:
                500, {'message': 'cannot read size information', 'errorMessage': 'size_not_exist'}
                : 상품 이미지 정보 등록 실패
        """
        sql = """
            SELECT
                id
                ,name
            FROM
                sizes
            ;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

            if not result:
                raise SizeNotExist('fail_to_get_size_list')

            return result

    def get_color_list(self, connection):
        """색상 정보 취득
            Args:
                connection: 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                return None

            History:
                2020-12-30(심원두): 초기 생성

            Raises:
                500, {'message': 'cannot read color information', 'errorMessage': 'color_not_exist'}
                : 상품 이미지 정보 등록 실패
        """
        sql = """
            SELECT
                id
                ,name
            FROM
                colors
            WHERE
                is_deleted = 0
            ;
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

            if not result:
                raise ColorNotExist('fail_to_get_color_list')

            return result

    def search_seller_list(self, connection, data):
        sql = """
            SELECT
                account_id
                ,name
                ,profile_image_url
            FROM
                sellers
            WHERE
                is_deleted = 0
                AND `name` LIKE %(seller_name)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            return result

    def get_main_category_list(self, connection):
        sql = """
            SELECT
                id
                ,`name`
            FROM
                main_categories
            WHERE
                is_deleted = 0
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            if not result:
                raise MainCategoryNotExist('fail_to_get_main_category_list')

            return result

    def get_sub_category_list(self, connection, data):
        sql = """
            SELECT
                sub_category.id
                ,sub_category.`name`
            FROM
                sub_categories as sub_category
                INNER JOIN main_categories as main_category
                    ON sub_category.main_category_id = main_category.id
            WHERE
                sub_category.is_deleted = 0
                AND main_category.id = %(main_category_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if not result:
                raise SubCategoryNotExist('fail_to_get_sub_category_list')

            return result