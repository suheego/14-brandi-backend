import pymysql

from utils.custom_exceptions import ProductNotExist, ProductImageNotExist, StockNotNotExist, ProductSearchListZero

class ProductManageDao:
    """ Persistence Layer
    
        Attributes: None
        
        Author: 심원두
        
        History:
            2020-12-31(심원두): 초기 생성
            2021-01-03(심원두): 상품 리스트 기능 구현, 상품 상세 정보 조회 기능 작성 중
    """

    def convert_where_condition(self, data):
        """상품 리스트 조회 기능. 특정 조건에 따른 유동적 조건문 작성
            
            Args:
                data : 비지니스 레이어에서 넘겨 받은 딕셔너리 객체
            
            Author: 심원두
            
            History:
                2020-12-31(심원두): 초기 생성
                2021-01-03(심원두): 초기 생성 및 검색 조건 별 쿼리문 생성 기능 작성
                
            Returns: where 조건 쿼리 + order by 쿼리 + offset limit 쿼리
            
            Raises:
                400, {'message': 'key error', 'errorMessage': format(e)} : 키에러
        """
        
        where_condition = ""
        
        try:
            if data['lookup_start_date'] and data['lookup_end_date']:
                where_condition += \
                    "AND product.updated_at " \
                    "BETWEEN CAST('{lookup_start_date} 00:00:00' AS DATETIME) " \
                    "AND CAST('{lookup_end_date} 23:59:59' AS DATETIME)" \
                    .format(
                        lookup_start_date=data['lookup_start_date'],
                        lookup_end_date  =data['lookup_end_date']
                    ) + '\n'
            
            if data['seller_name']:
                where_condition += "\t" + \
                    "AND seller.`name` = '{seller_name}'" \
                    .format(seller_name=data['seller_name']) + '\n'
            
            if data['product_name']:
                where_condition += "\t" + \
                    "AND product.`name` LIKE '%{product_name}%'" \
                    .format(product_name=data['product_name']) + '\n'
            
            if data['product_id']:
                where_condition += "\t" + \
                    "AND product.id = '{product_id}'" \
                    .format(product_id=data['product_id']) + '\n'
            
            if data['product_code']:
                where_condition += "\t" + \
                    "AND product.product_code = '{product_code}'" \
                    .format(product_code=data['product_code']) + '\n'
            
            if data['seller_attribute_type_id']:
                where_condition += "\t" + \
                    "AND seller_attribute_type.id = '{seller_attribute_type_id}'" \
                    .format(seller_attribute_type_id=data['seller_attribute_type_id']) + '\n'
            
            if data['is_sale']:
                where_condition += "\t" + \
                    "AND product.is_sale = '{is_sale}'" \
                    .format(is_sale=data['is_sale']) + '\n'
            
            if data['is_display']:
                where_condition += "\t" + \
                    "AND product.is_display = '{is_display}'" \
                    .format(is_display=data['is_display'])
            
            if data['is_discount']:
                where_condition += "\t" + \
                    "AND CASE WHEN product.discount_rate = {is_discount} " \
                    "THEN product.discount_rate = 0 " \
                    "ELSE product.discount_rate > 0 " \
                    "END " \
                    .format(is_discount=data['is_discount']) + '\n'
            
            # TODO: Login Decorator : seller sign-in not master
            # if not data.get('seller_id', None):
            #     where_condition += "\t" + \
            #        "AND product.seller_id = '{seller_id}'" \
            #        .format(seller_id=data['seller_id'])
            
            order_by = "\tORDER BY product.id DESC" + '\n'
            
            limit = "\tLIMIT {offset}, {limit};" \
                    .format(
                        offset=data['offset'],
                        limit =data['limit']
                    ) + '\n'
            
        except KeyError as e:
            raise e
        
        return where_condition + order_by + limit
    
    def get_total_products_count(self, connection, data):
        """상품 리스트 총 갯수 취득
        
            Args:
                connection : 데이터베이스 연결 객체
                data       : 비지니스 레이어에서 넘겨 받은 딕셔너리 객체
    
            Author: 심원두
    
            Returns:
                return result (상품 총 갯수)
    
            History:
                2020-12-31(심원두): 초기 생성
                2021-01-03(심원두): 상품 리스트 총 갯수 취득 기능 작성
            
            Raises: -
        """
        
        sql = """
        SELECT
            COUNT(*) AS total_count
        FROM
            PRODUCTS AS product
            INNER JOIN PRODUCT_IMAGES AS product_image
                ON product.id = product_image.product_id AND product_image.order_index = 1
            INNER JOIN SELLERS AS seller
                ON seller.account_id = product.seller_id
            INNER JOIN SELLER_ATTRIBUTE_TYPES AS seller_attribute_type
                ON seller_attribute_type.id = seller.seller_attribute_type_id
        WHERE
            product.is_deleted = 0
            AND product_image.is_deleted = 0
            AND product_image.order_index = 1
        """
        
        where_condition = self.convert_where_condition(data)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql + where_condition)
            result = cursor.fetchone()
            
            return result
    
    def search_products(self, connection, data):
        """상품 리스트 검색
        
            Args:
                connection: 데이터베이스 연결 객체
                data      : 비지니스 레이어에서 넘겨 받은 딕셔너리 객체
            
            Author: 심원두
            
            Returns: result (상품 정보 리스트)
            
            History:
                2020-12-31(심원두): 초기 생성
                2021-01-03(심원두): 상품 리스트 검색 쿼리 작성
                
            Raises:
                500, {'message': 'product search result zero', 'errorMessage': 'product_search_result_zero'} : 검색 결과 없음
        """
        
        sql = """
        SELECT
            product.updated_at AS 'updated_at'
            ,product_image.image_url AS 'product_image_url'
            ,product.`name` AS 'product_name'
            ,product.product_code AS 'product_code'
            ,product.id AS 'product_id'
            ,seller_attribute_type.`name` AS 'seller_attribute_type'
            ,seller.`name` AS 'seller_name'
            ,product.origin_price AS 'origin_price'
            ,product.discounted_price AS 'discounted_price'
            ,product.discount_rate AS 'discount_rate'
            ,product.is_sale AS 'is_sale'
            ,product.is_display AS 'is_display'
        FROM
            PRODUCTS AS product
            INNER JOIN PRODUCT_IMAGES AS product_image
                ON product.id = product_image.product_id AND product_image.order_index = 1
            INNER JOIN SELLERS AS seller
                ON seller.account_id = product.seller_id
            INNER JOIN SELLER_ATTRIBUTE_TYPES AS seller_attribute_type
                ON seller_attribute_type.id = seller.seller_attribute_type_id
        WHERE
            product.is_deleted = 0
            AND product_image.is_deleted = 0
            AND product_image.order_index = 1
        """
        
        where_condition = self.convert_where_condition(data)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql + where_condition)
            result = cursor.fetchall()
            
            if not result:
                raise ProductSearchListZero('product_search_result_zero')
            
            return result
    
    def get_product_detail(self, connection, data):
        """상품 상세 정보 조회
        
            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스 레이어에서 넘겨 받은 상품 검색에 사용될 키값
                
            Author: 심원두
            
            Returns: [{}]
            
            History:
                2021-01-02(심원두): 초기 생성
            
            Raises:
                500, {'message': '-', 'errorMessage': '-'} : --
        """
        
        sql = """
            SELECT
                `product_code` AS 'product_code'
                ,`is_sale` AS 'is_sale'
                ,`is_display` AS 'is_display'
                ,`main_category_id` AS 'main_category_id'
                ,`sub_category_id` AS 'sub_category_id'
                ,`is_product_notice` AS 'is_product_notice'
                ,`manufacturer` AS 'manufacturer'
                ,`manufacturing_date` AS 'manufacturing_date'
                ,`product_origin_type_id` AS 'product_origin_type_id'
                ,`name` AS 'product_name'
                ,`description` AS 'description'
                ,`detail_information` AS 'detail_information'
                ,`origin_price` AS 'origin_price'
                ,`discount_rate` AS 'discount_rate'
                ,`discounted_price` AS 'discounted_price'
                ,`discount_start_date` AS 'discount_start_date'
                ,`discount_end_date` AS 'discount_end_date'
                ,`minimum_quantity` AS 'minimum_quantity'
                ,`maximum_quantity` AS 'maximum_quantity'
                ,`updated_at` AS 'updated_at'
                ,`id` AS 'product_id'
            FROM
                products
            WHERE
                is_deleted = 0
                AND `product_code` = %(product_code)s
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchone()
            
            if not result:
                raise ProductNotExist('product_does_not_exist')
            
            return result
    
    def get_product_images(self, connection, data):
        """상품 이미지 리스트 검색
            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스 레이어에서 넘겨 받은 상품 이미지 취득에 사용될 키값
            Author: 심원두
            Returns: [{}]
            History:
                2021-01-02(심원두): 초기 생성
            Raises:
                500, {'message': '-',
                      'errorMessage': '-'} : --
        """
        sql = """
            SELECT
                id AS 'product_image_id'
                ,image_url AS 'image_url'
                ,order_index AS 'order_index'
            FROM
                product_images
            WHERE
                is_deleted = 0
                AND product_id = %(product_id)s
            ORDER BY
                order_index ASC;
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            
            if not result:
                raise ProductImageNotExist('product_image_does_not_exist')
            
            return result
    
    def get_product_options(self, connection, data):
        """상품 옵션 리스트 검색
            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스 레이어에서 넘겨 받은 상품 옵션 정보 취득에 사용될 키값
            Author: 심원두
            Returns: [{}]
            History:
                2021-01-02(심원두): 초기 생성
            Raises:
                500, {'message': '-',
                      'errorMessage': '-'} : --
        """
        sql = """
            SELECT
                stock.id AS 'stock_id'
                ,stock.product_option_code AS 'product_option_code'
                ,stock.remain AS 'remain'
                ,stock.`is_stock_manage` AS 'is_stock_manage'
                ,color.`id` AS 'color_id'
                ,color.`name` AS 'color_name'
                ,size.`id` AS 'size_id'
                ,size.`name` AS 'size_name'
            FROM
                stocks AS stock
                INNER JOIN colors AS color
                    ON stock.color_id = color.id
                INNER JOIN sizes AS size
                    ON stock.size_id = size.id
            WHERE
                stock.is_deleted = 0
                AND stock.product_id = %(product_id)s
            ORDER BY
                stock.product_option_code ASC;
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            
            if not result:
                raise StockNotNotExist('stock_does_not_exist')
    
            return result
