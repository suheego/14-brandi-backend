from datetime import datetime
from config                  import S3_BUCKET_URL
from utils.custom_exceptions import DateCompareException, LookUpDateFieldRequiredCheck


class ProductManageService:
    """ Business Layer

        Attributes:
            product_manage_dao : ProductManageDao 클래스

        Author: 심원두

        History:
            2020-12-31(심원두): 초기 생성
    """
    def __init__(self, product_manage_dao):
        self.product_manage_dao = product_manage_dao
        
    def search_product_service(self, connection, data):
        """ 특정 조건에 따른 product 검색
        
            Parameters:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 딕셔너리 객체
            
            Author: 심원두

            Returns:
                "result": {
                    "product_list": [
                        {
                            "discount_rate": 0.0,
                            "discounted_price": 10000.0,
                            "is_display": 1,
                            "is_sale": 1,
                            "origin_price": 10000.0,
                            "product_code": "P000000000000001131",
                            "product_id": 1131,
                            "product_image_url": "https://brandi-intern-8.s3.amazonaws.com/sellers/3/products/1131/images/flask.jpg",
                            "product_name": "상품이름",
                            "seller_attribute_type": "쇼핑몰",
                            "seller_name": "나는셀러3",
                            "updated_at": "2021-01-02 04:11:04"
                        }, ...
                    ],
                    "total_count": 951
            
            Raises:
                200, {'message': 'product search result zero',
                      'errorMessage': 'product_search_result_zero'} : 검색 결과 없음
                      
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)} : 잘못 입력된 키값
                      
                400, {'message': 'both date field required',
                      'errorMessage': 'both_date_field_required'} : 필수 값 유효성 검사
                      
                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_is_greater_than_end_date'} : 날짜 비교 유효성 검사
        """
        
        try:
            page_number = int(data['page_number'])
            limit       = int(data['limit'])
            
            if data['lookup_start_date'] and not data['lookup_end_date']:
                raise LookUpDateFieldRequiredCheck('both_date_field_required')

            if not data['lookup_start_date'] and data['lookup_end_date']:
                raise LookUpDateFieldRequiredCheck('both_date_field_required')
            
            if data['lookup_start_date'] and data['lookup_end_date']:
                if data['lookup_start_date'] > data['lookup_end_date']:
                    raise DateCompareException('start_date_is_greater_than_end_date')
            
            data['offset'] = (page_number * limit) - limit
            
            total_count  = self.product_manage_dao.get_total_products_count(
                                connection,
                                data
                            )['total_count']
            
            product_list = self.product_manage_dao.search_products(
                                connection,
                                data
                            )
            
            result = {
                'total_count'  : total_count,
                'product_list' : [
                    {
                        'updated_at'            : product['updated_at'],
                        'product_image_url'     : S3_BUCKET_URL + product['product_image_url'],
                        'product_name'          : product['product_name'],
                        'product_code'          : product['product_code'],
                        'product_id'            : product['product_id'],
                        'seller_attribute_type' : product['seller_attribute_type'],
                        'seller_name'           : product['seller_name'],
                        'origin_price'          : product['origin_price'],
                        'discounted_price'      : product['discounted_price'],
                        'discount_rate'         : product['discount_rate'],
                        'is_sale'               : product['is_sale'],
                        'is_display'            : product['is_display'],
                    } for product in product_list
                ]
            }
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def detail_product_service(self, connection, product_code):
        """ 해당 상품 코드의 상세 정보 취득

            Parameters:
                connection   : 데이터베이스 연결 객체
                product_code : View 에서 넘겨받은 상품 코드

            Author: 심원두

            Returns:
                -

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)} : 잘못 입력된 키값
        """
        
        data = dict()
        
        try:
            # 상품 정보
            data['product_code'] = product_code
            product_detail = self.product_manage_dao.get_product_detail(connection, data)

            print("======================")
            print(product_detail)
            
            # 상품 이미지 정보
            data['product_id'] = product_detail['product_id']
            product_images = self.product_manage_dao.get_product_images(connection, data)

            print("======================")
            print(product_images)
            # S3_BUCKET_URL
            
            # 상품 옵션 정보
            product_options = self.product_manage_dao.get_product_options(connection, data)
            
            print("======================")
            print(product_options)
            
            result = {
                'product_detail' : product_detail,
                'product_images' : [
                    {
                        'product_image_url' : S3_BUCKET_URL + image['product_image_url'],
                        'order_index'       : image['order_index']
                    } for image in product_images],
                'product_options' : [
                    {
                        'color_id'          : option['color_id'],
                        'size_id'           : option['size_id'],
                        'remain'            : option['remain']
                    } for option in product_options]
            }
            
            return result

        except Exception:
            raise Exception('알 수 없는 에러')