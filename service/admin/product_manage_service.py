from config                  import S3_BUCKET_URL
from utils.custom_exceptions import (
    DateCompareException,
    LookUpDateFieldRequiredCheck,
    SellerAttributeTypeException
)


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
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키 값
                      
                400, {'message': 'both date field required',
                      'errorMessage': 'both_date_field_required'}: 필수 값 유효성 체크 에러
                      
                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_is_greater_than_end_date'}: 날짜 비교 유효성 체크 에러
                
                400, {'message': 'invalid seller attribute type',
                      'errorMessage': 'invalid_seller_attribute_type'}: 셀러 타입 유효성 체크 에러
        """
        
        try:
            if data['lookup_start_date'] and not data['lookup_end_date']:
                raise LookUpDateFieldRequiredCheck('both_date_field_required')

            if not data['lookup_start_date'] and data['lookup_end_date']:
                raise LookUpDateFieldRequiredCheck('both_date_field_required')
            
            if data['lookup_start_date'] and data['lookup_end_date']:
                if data['lookup_start_date'] > data['lookup_end_date']:
                    raise DateCompareException('start_date_is_greater_than_end_date')
            
            if data['seller_attribute_type_ids']:
                for type_id in data['seller_attribute_type_ids']:
                    if type_id < 0 or type_id > 7:
                        raise SellerAttributeTypeException("invalid_seller_attribute_type")
            
            if data['product_name']:
                data['product_name'] = '%' + data['product_name'] + '%'
            
            data['page_number'] = int(data['page_number'])
            data['limit']       = int(data['limit'])
            
            data['offset']      = (data['page_number'] * data['limit']) - data['limit']
            
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
    
    def detail_product_service(self, connection, data):
        """ 해당 상품 코드의 상세 정보 취득
            
            Parameters:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 딕셔너리 객체 (상품 코드)
            
            Author: 심원두
            
            Returns:
                "result": {
                    "product_detail": {
                    "description": "상품 설명===999",
                    "detail_information": "html==============",
                    "discount_end_date": "2021-12-25 23:59:00",
                    "discount_rate": 0.1,
                    "discount_start_date": "2020-11-01 09:00:00",
                    "discounted_price": 9000.0,
                    "is_display": 1,
                    "is_product_notice": 0,
                    "is_sale": 1,
                    "main_category_id": 1,
                    "main_category_name": "아우터",
                    "manufacturer": "패션의 완성 위코드(제조)",
                    "manufacturing_date": "Wed, 01 Jan 2020 00:00:00 GMT",
                    "maximum_quantity": 20,
                    "minimum_quantity": 1,
                    "origin_price": 10000.0,
                    "product_code": "P0000000000000000999",
                    "product_id": 999,
                    "product_name": "성보의하루999",
                    "product_origin_type_id": 3,
                    "product_origin_type_name": "한국",
                    "sub_category_id": 6,
                    "sub_category_name": "무스탕/퍼",
                    "updated_at": "2020-12-31 13:25:08"
                },
                "product_images": [
                    {
                        "order_index": 1,
                        "product_image_url": "https://brandi-intern-8.s3.amazonaws.com/free-psd/simple-black
                    }
                ],
                "product_options": [
                    {
                        "color_id": 1,
                        "color_name": "Black",
                        "is_stock_manage": 0,
                        "product_option_code": "1194001008",
                        "remain": 100,
                        "size_id": 1,
                        "size_name": "Free",
                        "stock_id": 999
                    }
                ]
            }
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)} : 잘못 입력된 키값
                
                500, {'message': 'product does not exist',
                      'errorMessage': 'product_does_not_exist'} : 상품 정보 취득 실패
                      
                500, {'message': 'product image not exist',
                      'errorMessage': 'product_image_not_exist'}: 상품 이미지 정보 취득 실패
                
                500, {'message': 'stock info not exist',
                      'errorMessage': 'stock_does_not_exist'}: 옵션 정보 취득 실패
        """
        try:
            product_detail = self.product_manage_dao.get_product_detail(connection, data)
            
            data['product_id'] = product_detail['product_id']
            product_images     = self.product_manage_dao.get_product_images(connection, data)
            product_options    = self.product_manage_dao.get_product_options(connection, data)
            
            result = {
                'product_detail' : {
                    'product_code'             : product_detail['product_code'],
                    'is_sale'                  : product_detail['is_sale'],
                    'is_display'               : product_detail['is_display'],
                    'main_category_id'         : product_detail['main_category_id'],
                    'main_category_name'       : product_detail['main_category_name'],
                    'sub_category_id'          : product_detail['sub_category_id'],
                    'sub_category_name'        : product_detail['sub_category_name'],
                    'is_product_notice'        : product_detail['is_product_notice'],
                    'manufacturer'             : product_detail['manufacturer'],
                    'manufacturing_date'       : product_detail['manufacturing_date'].isoformat(),
                    'product_origin_type_id'   : product_detail['product_origin_type_id'],
                    'product_origin_type_name' : product_detail['product_origin_type_name'],
                    'product_name'             : product_detail['product_name'],
                    'description'              : product_detail['description'],
                    'detail_information'       : product_detail['detail_information'],
                    'origin_price'             : product_detail['origin_price'],
                    'discount_rate'            : product_detail['discount_rate'],
                    'discounted_price'         : product_detail['discounted_price'],
                    'discount_start_date'      : product_detail['discount_start_date'],
                    'discount_end_date'        : product_detail['discount_end_date'],
                    'minimum_quantity'         : product_detail['minimum_quantity'],
                    'maximum_quantity'         : product_detail['maximum_quantity'],
                    'updated_at'               : product_detail['updated_at'],
                    'product_id'               : product_detail['product_id'],
                },
                'product_images' : [
                    {
                        'product_image_url' : S3_BUCKET_URL + image['product_image_url'],
                        'order_index'       : image['order_index']
                    } for image in product_images
                ],
                'product_options': [
                    {
                        'stock_id'            : option['stock_id'],
                        'product_option_code' : option['product_option_code'],
                        'color_id'            : option['color_id'],
                        'color_name'          : option['color_name'],
                        'size_id'             : option['size_id'],
                        'size_name'           : option['size_name'],
                        'remain'              : option['remain'],
                        'is_stock_manage'     : option['is_stock_manage'],
                    } for option in product_options
                ]
            }
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
