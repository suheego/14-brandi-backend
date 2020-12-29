import pymysql

from utils.custom_exceptions import ProductCreateDenied, ProductImageCreateDenied

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
            return result # products 테이블에 신규 등록된 데이터의 pk (id) 값

        History:
            2020-12-29(심원두): 초기 생성

        Raises:
            400, {'message': 'user dose not exist', 'errorMessage': 'unable_to_create_product'}
            : products 테이블 데이터 생성 실패
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
                ,CAST(%(discount_rate)s/100 AS DECIMAL(3,2))
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
            result = cursor.lastrowid
            if not result:
                raise ProductCreateDenied('unable_to_create_product')
            
            return result
    
    def update_product_code(self, connection, data):
        """상품 정보 갱신

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 정보 갱신에 사용될 데이터
    
            Author: 심원두
    
            Returns:
                return result # 0 혹은 1 (0일 경우 갱신 실패, 1일 경우 데이터 갱신 성공)
    
            History:
                2020-12-29(심원두): 초기 생성
    
            Raises:
                400, {'message': 'user dose not exist', 'errorMessage': 'unable_to_update_product_code'}
                : products 테이블 product_code 갱신 실패
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
                raise ProductCreateDenied('unable_to_update_product_code')
            
            return result
    
    def insert_product_image(self, connection, data):
        sql = """
            INSERT INTO product_images(
                `image_url`
                , `product_id`
                , `order_index`
            ) VALUES (
                'product_image_url_1.png'
                , 1
                , 1
            );
        """
        
        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.lastrowid

            if not result:
                raise ProductImageCreateDenied('unable_to_create_product_image')

            return result
