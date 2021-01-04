import io
import base64

from PIL                     import Image
from werkzeug.utils          import secure_filename

from config                  import S3_BUCKET_URL
from utils.amazon_s3         import S3FileManager, GenerateFilePath
from utils.custom_exceptions import (
    RequiredFieldException,
    NotValidFileException,
    FileSizeException,
    FileExtensionException,
    CompareQuantityCheck,
    ComparePriceCheck,
    DateCompareException,
    FileScaleException,
    FileUploadFailException
)

class ProductCreateService:
    """ Business Layer

        Attributes:
            create_product_dao : CreateProductDao 클래스

        Author: 심원두

        History:
            2020-12-29(심원두): 초기 생성
            2020-12-30(심원두): 예외처리 추가
            2020-01-03(심원두): 이미지 등록 예외 처리 수정, 업로드 시 파일 손상 이슈 수정
    """
    
    def __init__(self, create_product_dao):
        self.create_product_dao = create_product_dao
    
    def create_product_service(self, connection, data):
        """ product 생성

            Parameters:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 dict 객체

            Author: 심원두
            
            Returns:
                product_id : 생성한 products 테이블의 키 값
                
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

                400, {'message': 'required field is blank',
                      'errorMessage': 'required_manufacture_information'}: 제조 정보 필드 없음
                
                400, {'message': 'required field is blank',
                      'errorMessage': 'required_discount_start_or_end_date'}: 필수 입력 항목 없음
                
                400, {'message': 'compare quantity field check error',
                      'errorMessage': 'minimum_quantity_cannot_greater_than_maximum_quantity'}: 최소 구매 수량이 최대 보다 큼
                
                400, {'message': 'compare price field check error',
                      'errorMessage': 'discounted_price_cannot_greater_than_origin_price'}: 할인가가 판매가 보다 큼

                400, {'message': 'compare price field check error',
                      'errorMessage': 'wrong_discounted_price'}: 판매가와 할인가 일치하지 않음
                
                400, {'message': 'compare price field check error',
                      'errorMessage': 'required_discount_start_or_end_date'}: 할인 시작, 종료 일자 필드 없음
                
                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_cannot_greater_than_end_date'}: 할인 시작일이 종료일 보다 큼
                
                400, {'message': 'compare price field check error',
                      'errorMessage': 'discounted_price_have_to_same_with_origin_price'}: 할인가, 판매가 불일치(할인율 0)
                
                500, {'message': 'product create denied',
                      'errorMessage': 'unable_to_create_product'}               : 상품 정보 등록 실패
            
            History:
                2020-12-29(심원두): 초기 생성
                2020-12-30(심원두): 예외처리 구현
                2020-01-03(심원두): 예외처리 추가/수정
        """
        try:
            if int(data['minimum_quantity']) != 0 and int(data['maximum_quantity']) != 0:
                if int(data['minimum_quantity']) > int(data['maximum_quantity']):
                    raise CompareQuantityCheck('minimum_quantity_cannot_greater_than_maximum_quantity')
            
            if int(data['minimum_quantity']) == 0:
                data['minimum_quantity'] = 1
            
            if int(data['maximum_quantity']) == 0:
                data['minimum_quantity'] = 20
            
            # 상품 고시 정보 0 일 경우, 하위 필드 값 None 치환
            if int(data['is_product_notice']) == 0:
                data['manufacturer'] = None
                data['manufacturing_date'] = None
                data['product_origin_type_id'] = None
                
            else:
                # 상품 고시 정보 1일 경우 하위 필드 값 필수 필드 체크
                if not data['manufacturer'] or not data['manufacturing_date'] or not data['product_origin_type_id']:
                    raise RequiredFieldException('required_manufacture_information')
            
            # 할인율 0 일 경우, 할인가 = 판매가 처리
            if int(data['discount_rate']) == 0:
                data['discounted_price'] = data['origin_price']
                data['discount_start_date'] = None
                data['discount_end_date'] = None
                
            else:
                
                # 할인율 0 이 아닐 경우
                if float(data['discounted_price']) > float(data['origin_price']):
                    raise ComparePriceCheck('discounted_price_cannot_greater_than_origin_price')
                
                # [판매가 - 할인가격 != 할인가] 의 경우
                if (float(data['origin_price']) * (1 - float(data['discount_rate']) / 100)) != \
                    float(data['discounted_price']):
                    raise ComparePriceCheck('wrong_discounted_price')
                
                # 할인율이 0이 아닌 경우, [할인 시작 일자, 할이 종료 일자] 필수 체크
                if data['discount_start_date'] and not data['discount_end_date']:
                    raise RequiredFieldException('required_discount_start_or_end_date')
                
                if not data['discount_start_date'] and data['discount_end_date']:
                    raise RequiredFieldException('required_discount_start_or_end_date')
                
                if data['discount_start_date'] and data['discount_end_date']:
                    
                    if data['discount_start_date'] > data['discount_end_date']:
                        
                        raise DateCompareException('start_date_cannot_greater_than_end_date')
                else:
                    data['discount_start_date'] = None
                    data['discount_end_date'] = None
            
            data['discount_rate'] = float(data['discount_rate']) / 100
            
            #TODO : HTML with image 파일 DB 저장
            # 1. encode 방법
            # html = payload['detail_information']
            # encode = html.encode("utf-8")
            # payload['detail_information'] = encode
            # 2. base64 방법
            # html = payload['detail_information']
            # encode = base64.b64encode(html.encode()).decode()
            # payload['detail_information'] = encode
            
            return self.create_product_dao.insert_product(connection, data)
            
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def update_product_code_service(self, connection, product_id):
        """ 상품 코드(product_code) 생성 후 상품 코드 업데이트

            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 해당 상품 정보 테이블의 id

            Author: 심원두
            
            Returns:
                0: 상품 코드 갱신 실패
                1: 상품 코드 갱신 성공

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

                500, {'message': 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'}: 상품 코드 갱신 실패
            
            History:
                2020-12-29(심원두): 초기 생성
        """
        try:
            
            # 상품 코드 생성
            data = {
                'product_code' : 'P' + str(product_id).zfill(18),
                'product_id'   : product_id
            }
            
            return self.create_product_dao.update_product_code(connection, data)
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e

    def create_product_images_service(self, connection, seller_id, product_id, product_images):
        """ 상품 이미지 등록
            
            Args:
                'connection'     : 데이터베이스 연결 객체
                'seller_id'      : View 에서 넘겨 받은 셀러 아이디
                'product_id'     : View 에서 넘겨 받은 상품 아이디
                'product_images' : View 에서 넘겨 받은 이미지 파일
            
            Author: 심원두
            
            Returns:
                0: 상품 이미지 테이블 등록 실패
                1: 상품 이미지 테이블 등록 성공

            Raises:
                413, {'message': 'invalid file',
                      'errorMessage': 'invalid_file'}: 파일 이름이 공백, 혹은 파일을 정상적으로 받지 못함
                
                413, {'message': 'file size too large',
                      'errorMessage': 'file_size_too_large'}: 파일 사이즈 정책 위반 (4메가 이상인 경우)
                
                413, {'message': 'file scale too small, 640 * 720 at least',
                      'errorMessage': 'file_scale_at_least_640*720'}: 파일 스케일 정책 위반 (680*720 미만인 경우)

                413, {'message': 'only allowed jpg type',
                      'errorMessage': 'only_allowed_jpg_type'}: 파일 확장자 정책 위반 (JPG, JPEG 아닌 경우)
                
                500, {'message': 'image_file_upload_to_amazon_fail',
                      'errorMessage': 'image_file_upload_fail'}: 이미지 업로드 실패

                500, {'message': 'product image create denied',
                      'errorMessage': 'unable_to_create_product_image'}: 상품 이미지 등록 실패
            
            History:
                2020-12-29(심원두): 초기 생성
                2020-01-03(심원두): 이미지 업로드 예외 처리 수정, 파일 손상 이슈 수정
        """
        try:
            for index, product_image in enumerate(product_images):
                
                if not product_image or not product_image.filename:
                    raise NotValidFileException('invalid_file')
                
                # 바이트 객체
                buffer = io.BytesIO()
                # 이미지 열기 (읽기 모드)
                image = Image.open(product_image, 'r')
                # 임시 저장
                image.save(buffer, image.format)
                # 포인터 리와인드
                buffer.seek(0)
                
                # 파일 크기 체크 (4메가 이상인 경우 에러)
                if buffer.getvalue().__sizeof__() > 4194304:
                    raise FileSizeException('file_size_too_large')
                
                # 파일 사이즈(가로, 세로) 체크 (640*720 미만인 경우 에러)
                # if image.size[0] < 640 or image.size[1] < 720:
                #     raise FileScaleException('file_scale_at_least_640*720')
                
                # 파일 확장자 체크 (JPEG, JPG 허용)
                if image.format != "JPEG":
                    raise FileExtensionException('only_allowed_jpg_type')
                
                # 이미지 파일 패스 생성
                file_path = GenerateFilePath().generate_file_path(
                    3,
                    seller_id  = seller_id,
                    product_id = product_id
                )
                
                # 아마존 업로더
                url = S3FileManager().file_upload(
                    buffer,
                    file_path + secure_filename(product_image.filename)
                )
                
                # 아마존 업로드 후 url 리턴 받지 못한 경우
                if not url:
                    raise FileUploadFailException('image_file_upload_fail')
                
                data = {
                    'image_url'   : url,
                    'product_id'  : product_id,
                    'order_index' : index
                }
                
                self.create_product_dao.insert_product_image(connection, data)
        
        except Exception as e:
            raise e
    
    def create_stock_service(self, connection, product_id, stocks):
        """ 상품 옵션 정보 등록
            
            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id
                stocks     : View 에서 넘겨 받은 상품 옵션 정보
            
            Author: 심원두
            
            Returns:
                0: 옵션 테이블 등록 실패
                1: 옵션 테이블 등록 성공
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

                500, {'message': 'stock create denied',
                      'errorMessage': 'unable_to_create_stocks'}: 상품 옵션 정보 등록 실패
            
            History:
                2020-12-29(심원두): 초기 생성
                2020-01-03(심원두): 프론트엔드 상의 후 재고 관리 컬럼 추가에 대한 대응
        """
        try:
            data = {}
            
            for stock in stocks:
                # 상품 옵션 코드 생성
                product_option_code = \
                    str(product_id) + \
                    str(stock['color']).zfill(3) + \
                    str(stock['size']).zfill(3)
                
                data['product_option_code'] = product_option_code
                data['product_id']          = product_id
                data['color_id']            = stock['color']
                data['size_id']             = stock['size']
                data['remain']              = stock['remain']
                
                if not stock['isStockManage']:
                    stock['isStockManage'] = 0

                data['is_stock_manage'] = stock['isStockManage']
                
                if not stock['remain']:
                    data['remain'] = 0
                
                self.create_product_dao.insert_stock(connection, data)
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def create_product_history_service(self, connection, product_id, data):
        """ 상품 이력 정보 등록

            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id
                data       : View 에서 넘겨 받은 상품 정보

            Author: 심원두

            Returns:
                0: 상품 이력 정보 등록 실패
                1: 상품 이력 정보 등록 성공
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

                500, {'message': 'product history create denied',
                      'errorMessage': 'unable_to_create_product_history'}: 상품 이력 등록 실패
            
            History:
                2020-12-29(심원두): 초기 생성
        """
        try:
            data['product_id']    = product_id
            data['discount_rate'] = float(data['discount_rate'])/100
            
            if not data['discount_start_date']:
                data['discount_start_date'] = None
            
            if not data['discount_end_date']:
                data['discount_end_date'] = None
            
            if not data['discounted_price']:
                data['discounted_price'] = None
            
            return self.create_product_dao.insert_product_history(connection, data)
            
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def create_product_sales_volumes_service(self, connection, product_id):
        """ 상품 판매량 정보 초기 등록

            Args:
                connection : 데이터 베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id

            Author: 심원두

            Returns:
                0: 상품 판매량 정보 초기 등록 실패
                1: 상품 판매량 정보 초기 등록 성공
            
            Raises:
                500, {'message': 'product history create denied',
                      'errorMessage': 'unable_to_create_product_history'}: 상품 이력 등록 실패
            
            History:
                2020-12-29(심원두): 초기 생성
        """
        try:
            return self.create_product_dao.insert_product_sales_volumes(connection, product_id)
        
        except Exception as e:
            raise e
        
    def main_category_list_service(self, connection):
        """ 메인 카테고리 정보 취득
            
            Args:
                connection : 데이터 베이스 연결 객체
            
            Author: 심원두
            
            Returns:
                "result": [
                    {
                        "main_category_id": 1,
                        "main_category_name": "아우터"
                    },
                    {
                        "main_category_id": 2,
                        "main_category_name": "상의"
                    },
                ]
            
            Raises:
                500, {'message': 'fail to get main category list',
                      'errorMessage': 'fail_to_get_main_category_list'}: 메인 카테고리 정보 취득 실패
            
            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        try:
            main_category_list = self.create_product_dao.get_main_category_list(connection)
            
            result = [
                {
                    'main_category_id'  : main_category_info['id'],
                    'main_category_name': main_category_info['name']
                } for main_category_info in main_category_list
            ]
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e

    def get_color_list_service(self, connection):
        """ 색상 리스트 취득
            
            Args:
                connection : 데이터 베이스 연결 객체

            Author: 심원두

            Returns:
                "result": [
                    {
                        "color_id": 1,
                        "color_name": "Black"
                    },
                    {
                        "color_id": 2,
                        "color_name": "White"
                    },
                ]

            Raises:
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패
            
            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        try:
            color_list = self.create_product_dao.get_color_list(connection)
            
            result = [
                {
                    'color_id'  : color['id'],
                    'color_name': color['name']
                } for color in color_list
            ]
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def get_size_list_service(self, connection):
        """ 사이즈 리스트 취득
            
            Args:
                connection : 데이터 베이스 연결 객체

            Author: 심원두

            Returns:
                [
                    {
                        "color_id": 1,
                        "color_name": "Black"
                    },
                    {
                        "color_id": 2,
                        "color_name": "White"
                    },
                ]
            
            Raises:
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패

            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        try:
            size_list = self.create_product_dao.get_size_list(connection)
            
            result = [
                {
                    'size_id'  : size['id'],
                    'size_name': size['name']
                } for size in size_list
            ]
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def get_product_origin_types_service(self, connection):
        """ 원산지 리스트 취득

            Args:
                connection : 데이터 베이스 연결 객체

            Author: 심원두

            Returns:
                [
                    {
                        "product_origin_type_id": 1,
                        "product_origin_type_name": "기타 "
                    },
                    {
                        "product_origin_type_id": 2,
                        "product_origin_type_name": "중국"
                    },
                ]
            
            Raises:
                500, {'message': 'fail to get product origin types',
                      'errorMessage': 'fail_to_get_product_origin_types'} : 원산지 정보 취득 실패

            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        try:
            product_origin_types = self.create_product_dao.get_product_origin_types(connection)
            
            result = [
                {
                    'product_origin_type_id'  : product_origin_type['id'],
                    'product_origin_type_name': product_origin_type['name']
                } for product_origin_type in product_origin_types
            ]
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def search_seller_list_service(self, connection, data):
        """ 셀러 리스트 취득
            
            Args:
                connection : 데이터 베이스 연결 객체
                data       : View 에서 넘겨 받은 셀러명
            Author: 심원두

            Returns:
                [
                    {
                        "profile_image_url": "https://brandi-intern-8.s3.amazonaws.co...,
                        "seller_id": 10,
                        "seller_name": "나는셀러10"
                    },
                    {
                        "profile_image_url": "https://brandi-intern-8.s3.amazonaws.co...
                        "seller_id": 100,
                        "seller_name": "나는셀러100"
                    },

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        try:
            if data['seller_name']:
                data['seller_name'] = '%' + data['seller_name'] + '%'
            
            seller_info = \
                self.create_product_dao.search_seller_list(
                    connection,
                    data
                )
            
            result = [
                {
                    'seller_id'         : seller['seller_id'],
                    'seller_name'       : seller['seller_name'],
                    'profile_image_url' : S3_BUCKET_URL + seller['profile_image_url']
                } for seller in seller_info
            ]
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def get_sub_category_list_service(self, connection, data):
        """ 셀러 리스트 취득
            
            Args:
                connection : 데이터 베이스 연결 객체
                data       : View 에서 넘겨 받은 메인 카테고리 아이디
            
            Author: 심원두
            
            Returns:
                [
                    {
                        "sub_category_id": 13,
                        "sub_category_name": "청바지"
                    },
                    {
                        "sub_category_id": 14,
                        "sub_category_name": "슬랙스"
                    },
                ]
            
            Raises:
                500, {'message': 'fail to get sub category list',
                      'errorMessage': 'fail_to_get_sub_category_list'}: 색상 정보 취득 실패
            
            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        try:
            sub_category_list = \
                self.create_product_dao.get_sub_category_list(
                    connection,
                    data
                )
            
            result = [
                {
                    'sub_category_id'   : sub_category['sub_category_id'],
                    'sub_category_name' : sub_category['sub_category_name'],
                } for sub_category in sub_category_list
            ]
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
