import traceback
import pymysql

from utils.custom_exceptions import (
    ProductCreateDenied,
    ProductCodeUpdatedDenied,
    ProductImageCreateDenied,
    StockCreateDenied,
    ProductHistoryCreateDenied,
    ProductSalesVolumeCreateDenied,
    ProductOriginTypesNotExist,
    ColorNotExist,
    SizeNotExist,
    MainCategoryNotExist,
    SubCategoryNotExist
)

class ProductCreateDao:
    """ Persistence Layer

        Attributes: None

        Author: 심원두

        History:
            2020-12-29(심원두): 초기 생성
            2020-01-03(심원두): 1차 수정. 프론트엔드와 맞춘 후 쿼리 수정
    """
    
    def insert_product(self, connection, data):
        """ 상품 정보 등록 (상품 정보 테이블)
        
        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받은 products 테이블 등록에 사용될 데이터
        
        Author: 심원두
        
        Returns:
            product_id : products 테이블에 신규 등록된 id 값
        
        History:
            2020-12-29(심원두): 초기 생성
            2020-12-31(심원두): Docstring 수정
        
        Raises:
            500, {'message': 'product create denied',
                  'errorMessage': 'unable_to_create_product'} : 상품 정보 등록 실패
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
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                product_id = cursor.lastrowid
                
                if not product_id:
                    raise ProductCreateDenied('unable_to_create_product')
                
                return product_id
        
        except ProductCreateDenied as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
    
    def update_product_code(self, connection, data):
        """ 상품 정보 갱신 (product_code 갱신)
            
            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 products 테이블 갱신에 사용될 데이터
            
            Author: 심원두
            
            Returns:
                0 : products 테이블 갱신 실패
                1 : products 테이블 갱신 성공 (product_code)
            
            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정
            
            Raises:
                500, {'message': 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'} : 상품 코드 갱신 실패
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
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                
                if not result:
                    traceback.print_exc()
                    raise ProductCodeUpdatedDenied('unable_to_update_product_code')

        except ProductCodeUpdatedDenied as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
    
    def insert_product_image(self, connection, data):
        """ 상품 이미지 정보 등록
            
            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 product_images 테이블 등록에 사용될 데이터

            Author: 심원두

            Returns:
                0 : products_images 테이블 데이터 생성 실패
                1 : products_images 테이블 데이터 생성 성공

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'product image create denied',
                      'errorMessage': 'unable_to_create_product_image'} : 상품 이미지 정보 등록 실패
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
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.lastrowid
                
                if not result:
                    traceback.print_exc()
                    raise ProductImageCreateDenied('unable_to_create_product_image')
                
                return result
        
        except ProductImageCreateDenied as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
    
    def insert_stock(self, connection, data):
        """ 상품 옵션 정보 등록

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 옵션 정보 이미지 등록에 사용될 데이터

            Author: 심원두

            Returns:
                0 : stocks 테이블 데이터 생성 실패
                1 : stocks 테이블 데이터 생성 성공

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'stock create denied', 'errorMessage': 'unable_to_create_stocks'}
                : 상품 이미지 정보 등록 실패
        """
        sql = """
            INSERT INTO stocks(
                 `product_option_code`
                , `is_stock_manage`
                , `remain`
                , `color_id`
                , `size_id`
                , `product_id`
            ) VALUES (
                %(product_option_code)s
                ,%(is_stock_manage)s
                ,%(remain)s
                ,%(color_id)s
                ,%(size_id)s
                ,%(product_id)s
            );
        """
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                
                if not result:
                    traceback.print_exc()
                    raise StockCreateDenied('unable_to_create_stocks')
                
                return result
        
        except StockCreateDenied as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
    
    def insert_product_history(self, connection, data):
        """ 상품 이력 정보 등록
            
            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 옵션 정보 이미지 등록에 사용될 데이터
            
            Author: 심원두
            
            Returns:
                0 : product_histories 테이블 데이터 생성 실패
                1 : product_histories 테이블 데이터 생성 성공
            
            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정
            
            Raises:
                500, {'message': 'product history create denied',
                      'errorMessage': 'unable_to_create_product_history'} : 상품 이미지 정보 등록 실패
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
            );
        """
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
    
                if not result:
                    raise ProductHistoryCreateDenied('unable_to_create_product_history')
                
                return result
        
        except ProductHistoryCreateDenied as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
            
    
    def insert_product_sales_volumes(self, connection, product_id):
        """ 상품 판매량 정보 초기 등록
            
            Args:
                connection : 데이터베이스 연결 객체
                product_id : 서비스 레이어에서 넘겨 받은 product_sales_volumes 테이블 데이터 생성에 사용될 값
            
            Author: 심원두
            
            Returns:
                0 : product_sales_volumes 테이블 데이터 생성 실패
                1 : product_sales_volumes 테이블 데이터 생성 성공
            
            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정
            
            Raises:
                500, {'message': 'product sales volume create denied',
                      'errorMessage': 'unable_to_create_product_sales_volumes'} : 상품 판매량 정보 생성 실패
        """
        sql = """
            INSERT INTO product_sales_volumes (
                `product_id`
            ) VALUES (
                %s
            );
        """
        
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, product_id)
                
                if not result:
                    raise ProductSalesVolumeCreateDenied('unable_to_create_product_sales_volumes')
                
                return result
        
        except ProductSalesVolumeCreateDenied as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
    
    def get_product_origin_types(self, connection):
        """ 원산지 정보 취득
        
            Args:
                connection : 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                result : product_origin_types 테이블의 키, 원산지명

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'fail to get product origin types',
                      'errorMessage': 'fail_to_get_product_origin_types'} : 원산지 정보 취득 실패
        """
        sql = """
            SELECT
                id
                ,name
            FROM
                product_origin_types
            WHERE
                is_deleted = 0
            ORDER BY
                id;
        """
        
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                
                if not result:
                    raise ProductOriginTypesNotExist('fail_to_get_product_origin_types')
                
                return result
        
        except ProductOriginTypesNotExist as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e

    def get_size_list(self, connection):
        """사이즈 정보 취득
        
            Args:
                connection: 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                result : 테이블에서 취득한 사이즈 정보의 키, 사이즈명

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정
            
            Raises:
                500, {'message': 'fail to get size list',
                      'errorMessage': 'fail_to_get_size_list'} : 사이즈 정보 취득 실패
        """
        sql = """
            SELECT
                id
                ,name
            FROM
                sizes
            WHERE
                is_deleted = 0
            ORDER BY
                id;
        """
        
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
    
                if not result:
                    raise SizeNotExist('fail_to_get_size_list')
    
                return result
        
        except SizeNotExist as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e

    def get_color_list(self, connection):
        """ 색상 정보 취득
        
            Args:
                connection: 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                result : colors 테이블에서 취득한 색상 정보의 키, 색상명

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정
            
            Raises:
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패
        """
        sql = """
            SELECT
                id
                ,name
            FROM
                colors
            WHERE
                is_deleted = 0
            ORDER BY
                id;
        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                
                if not result:
                    raise ColorNotExist('fail_to_get_color_list')
    
                return result
        
        except ColorNotExist as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e

    def search_seller_list(self, connection, data):
        """셀러 정보 취득 (전방 일치 검색)
        
            Args:
                connection: 데이터베이스 연결 객체
                data      : 셀러 검색에 사용될 데이터

            Author: 심원두

            Returns:
                result : sellers 테이블에서 취득한 셀러 정보

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정
            
        """
        sql = """
            SELECT
                account_id AS 'seller_id'
                ,`name` AS 'seller_name'
                ,profile_image_url AS 'profile_image_url'
            FROM
                sellers
            WHERE
                is_deleted = 0
                AND `name` LIKE %(seller_name)s
            ORDER BY name
        """
        
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result
        
        except Exception as e:
            traceback.print_exc()
            raise e
    
    def get_main_category_list(self, connection):
        """ 메인 카테고리 정보 취득
        
            Args:
                connection: 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                result : main_categories 테이블에서 취득한 키, 카테고리명

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정
            
            Raises:
                500, {'message': 'fail to get main category list',
                      'errorMessage': 'fail_to_get_main_category_list'}: 메인 카테고리 정보 취득 실패
        """
        sql = """
            SELECT
                id
                ,`name`
            FROM
                main_categories
            WHERE
                is_deleted = 0
            ORDER BY
                id;
        """
        
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                if not result:
                    raise MainCategoryNotExist('fail_to_get_main_category_list')
    
                return result
        
        except MainCategoryNotExist as e:
            raise e
        
        except Exception as e:
            raise e
    
    def get_sub_category_list(self, connection, data):
        """ 메인 카테고리에 따른 서브 카테고리 정보 취득
        
            Args:
                connection: 데이터베이스 연결 객체
                data      : 메인 카테고리에 따른 서브 카테고리 정보를 얻기 위한 데이터
                
            Author: 심원두

            Returns:
                result : sub_categories 테이블에서 취득한 키, 카테고리명

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정

            Raises:
                500, {'message': 'fail to get sub category list',
                      'errorMessage': 'fail_to_get_sub_category_list'}: 색상 정보 취득 실패
        """
        sql = """
            SELECT
                sub_category.id AS 'sub_category_id'
                ,sub_category.`name` AS 'sub_category_name'
            FROM
                sub_categories as sub_category
                INNER JOIN main_categories as main_category
                    ON sub_category.main_category_id = main_category.id
            WHERE
                sub_category.is_deleted = 0
                AND main_category.id = %(main_category_id)s
        """
        
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                
                if not result:
                    raise SubCategoryNotExist('fail_to_get_sub_category_list')
    
                return result
        
        except SubCategoryNotExist as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
