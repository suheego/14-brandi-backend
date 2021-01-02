import fleep
import base64
from werkzeug.utils          import secure_filename

from utils.amazon_s3         import S3FileManager, GenerateFilePath
from utils.custom_exceptions import (
    CorrelationCheckException,
    RequiredFieldException,
    NotValidFileException,
    FileSizeException,
    FileExtensionException
)


class ProductCreateService:
    """ Business Layer

        Attributes:
            create_product_dao : CreateProductDao 클래스

        Author: 심원두

        History:
            2020-12-29(심원두): 초기 생성
            2020-12-30(심원두): 예외처리 추가
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
                      'errorMessage': 'key_error' + format(e)}                  : 잘못 입력된 키값

                400, {'message': 'required field is blank',
                      'errorMessage': 'required_field_check_fail'}              : 필수 입력 항목 에러

                400, {'message': 'correlation check fail',
                      'errorMessage': '_minimum_quantity_maximum_quantity'}     : 최소구매, 최대구매 수량 비교

                400, {'message': 'correlation check fail',
                      'errorMessage': '_discounted_price_origin_price'}         : 판매가, 할인가 비교

                400, {'message': 'correlation check fail',
                      'errorMessage': '_discount_start_date__discount_end_date'}: 할인 시작일, 할인 종료일 비교

                500, {'message': 'product create denied',
                      'errorMessage': 'unable_to_create_product'}               : 상품 정보 등록 실패

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-30(심원두): 예외처리 구현
        """
        try:
            # is_product_notice      = data['is_product_notice']
            # manufacturer           = data['manufacturer']
            # manufacturing_date     = data['manufacturing_date']
            # product_origin_type_id = data['product_origin_type_id']
            # minimum_quantity       = data['minimum_quantity']
            # maximum_quantity       = data['maximum_quantity']
            # origin_price           = data['origin_price']
            # discount_rate          = data['discount_rate']
            # discounted_price       = data['discounted_price']
            # discount_start_date    = data['discount_start_date']
            # discount_end_date      = data['discount_end_date']
            #
            # print('상품 등록 서비스1')
            #
            # # is_product_notice 가 True 일 때 하위 항목 필수 입력 처리
            # if int(is_product_notice):
            #     if not manufacturer or not manufacturing_date or not product_origin_type_id:
            #         raise RequiredFieldException('required_field_check_fail')
            #
            # print('상품 등록 서비스2')
            # # 최소 판매량, 최대 판매량 비교 예외처리
            # if int(minimum_quantity) > int(maximum_quantity):
            #     raise CorrelationCheckException(
            #         '_minimum_quantity' +
            #         '_maximum_quantity'
            #     )
            #
            # print('상품 등록 서비스3')
            # # 기본 판매가격, 할인 판매 가격 비교 예외처리
            # if not discounted_price:
            #     discounted_price = 0
            #
            # if int(discounted_price) > int(origin_price):
            #     raise CorrelationCheckException(
            #         '_discounted_price' +
            #         '_origin_price'
            #     )
            #
            # print('상품 등록 서비스4')
            # # 세일 시작 날짜가 존재할 경우, 세일 종료 날짜 필수 항목 예외처리
            # if discount_start_date:
            #     if not discount_end_date:
            #         raise RequiredFieldException('required_field_check_fail')
            #
            # print('상품 등록 서비스5')
            # # 세일 종료 날짜가 존재할 경우, 세일 시작 날짜 필수 항목 예외처리
            # if discount_end_date:
            #     if not discount_start_date:
            #         raise RequiredFieldException('required_field_check_fail')
            #
            # print('상품 등록 서비스6')
            # # 세일 시작 날짜, 세일 종료 날짜 비교 예외처리
            # if discount_start_date > discount_end_date:
            #     raise CorrelationCheckException(
            #         '_discount_start_date' +
            #         '_discount_end_date'
            #     )
            #
            # print('상품 등록 서비스7')
            # # 할인율 Decimal(3,2)
            # data['discount_rate'] = float(data['discount_rate']) / 100
            
            payload = dict()
            # payload['seller_id']              = data['seller_id']
            # payload['account_id']             = data['account_id']
            # payload['is_sale']                = data['is_sale']
            # payload['is_display']             = data['is_display']
            # payload['main_category_id']       = data['main_category_id']
            # payload['sub_category_id']        = data['sub_category_id']
            # payload['is_product_notice']      = data['is_product_notice']
            # payload['manufacturer']           = data['manufacturer']
            # payload['manufacturing_date']     = data['manufacturing_date']
            # payload['product_origin_type_id'] = data['product_origin_type_id']
            # payload['product_name']           = data['product_name']
            # payload['description']            = data['description']
            payload['detail_information']     = data['detail_information']
            # payload['minimum_quantity']       = data['minimum_quantity']
            # payload['maximum_quantity']       = data['maximum_quantity']
            # payload['origin_price']           = data['origin_price']
            # payload['discount_rate']          = data['discount_rate']
            # payload['discounted_price']       = data['discounted_price']
            # payload['discount_start_date']    = data['discount_start_date']
            # payload['discount_end_date']      = data['discount_end_date']
            
            # if not data.get('manufacturing_date'):
            #     payload['manufacturing_date'] = None
            #
            # if not data.get('product_origin_type_id'):
            #     payload['product_origin_type_id'] = None
            #
            # if not data.get('discount_start_date'):
            #     payload['discount_start_date'] = None
            #
            # if not data.get('discount_end_date'):
            #     payload['discount_end_date'] = None
            #
            # if not data.get('discounted_price'):
            #     payload['discounted_price'] = 0.0
            
            # print('payload::', payload)
            # payload['detail_information'] = ""
            
            # 1번째 시도
            html = payload['detail_information']
            # encode = base64.b64encode(html)
            encode = html.encode("utf-8")
            print(encode)
            
            # payload['detail_information'] = html
            payload['detail_information'] = encode
            
            # html = payload['detail_information']
            # print('html::', type(html), html)
            #
            # a = base64.b64encode(html.encode()).decode()
            # print('encoded::', a)
            # payload['detail_information'] = a

            # encoded = base64.b64decode(html.encode().decode())
            
            print('상품 등록 서비스8')
            return self.create_product_dao.insert_product(connection, payload)

        except KeyError:
            raise KeyError('key_error')

    def update_product_code_service(self, connection, product_id):
        """ 상품 코드(product_code) 생성 후 상품 코드 업데이트

            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 해당 상품 정보 테이블의 id

            Author: 심원두

            Returns:
                None

            Raises:
                400, {'message'     : 'key error',
                      'errorMessage': 'key_error' + format(e)}        : 잘못 입력된 키값

                500, {'message'     : 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'}: 상품 코드 갱신 실패

            History:
                2020-12-29(심원두): 초기 생성
        """

        try:
            data = dict()
            print("상품 코드 수정 서비스1")
            # 상품 코드 생성
            data['product_code'] = 'P' + str(product_id).zfill(18)
            data['product_id']   = product_id

            print("상품 코드 수정 서비스2")
            # 상품 코드 업데이트 DAO 호출
            self.create_product_dao.update_product_code(connection, data)
            
        except KeyError:
            raise KeyError('key_error')

    def create_product_images_service(self, connection, seller_id, product_id, product_images):
        """ 상품 이미지 등록

            Args:
                connection     : 데이터베이스 연결 객체
                product_id     : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id
                product_images : View 에서 넘겨 받은 이미지 파일

            Author: 심원두

            Returns:
                None

            Raises:
                400, {'message'     : 'key error',
                      'errorMessage': 'key_error' + format(e)}         : 잘못 입력된 키값

                400, {'message'     : 'invalid file',
                      'errorMessage': 'key_error' + format(e)}         : 유효하지 않은 파일

                400, {'message'     : 'only allowed jpg type',
                      'errorMessage': 'key_error' + format(e)}         : 유효하지 않은 파일 확장자

                413, {'message'     : 'file size too large',
                      'errorMessage': 'key_error' + format(e)}         : 파일 사이즈 정책 위반

                500, {'message'     : 'product image create denied',
                      'errorMessage': 'unable_to_create_product_image'}: 상품 이미지 등록 실패

            History:
                2020-12-29(심원두): 초기 생성
        """

        try:
            data = dict()
            print("상품 이미지 서비스1")
            for index, image in enumerate(product_images):
    
                print("상품 이미지 서비스2")
                # 이미지 파일 존재 유효성 검사
                if not image or not image.filename:
                    print("===")
                    raise NotValidFileException('invalid_file')

                print("상품 이미지 서비스3")
                # 확장자 체크 (이미지 손상됨)
                # info = fleep.get(image.read(128))
                # if info.extension[0] != 'jpg':
                #     raise FileExtensionException('only_allowed_jpg_type')
                
                # 파일 사이즈 체크 (이미지 파일 잃어버림)
                # if len(image.read()) > 4194304:
                #     raise FileSizeException('file_size_too_large')
                
                # TODO : check image size(640, 720)

                print("상품 이미지 서비스4")
                file_path = GenerateFilePath().generate_file_path(
                    3,
                    seller_id  = seller_id,
                    product_id = product_id
                )
                
                secured_file_name = secure_filename(image.filename)

                print("상품 이미지 서비스5")
                # save to AMAZON S3
                url = S3FileManager().file_upload(image, file_path + secured_file_name)
                
                if url:
                    data['image_url']   = url
                    data['product_id']  = product_id
                    data['order_index'] = index

                    print("상품 이미지 서비스6")
                    self.create_product_dao.insert_product_image(connection, data)

        except KeyError:
            raise KeyError('key_error')

    def create_stock_service(self, connection, product_id, stocks):
        """ 상품 옵션 정보 등록

            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id
                stocks     : View 에서 넘겨 받은 상품 옵션 정보

            Author: 심원두

            Returns:
                None

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}  : 잘못 입력된 키값

                500, {'message': 'stock create denied',
                      'errorMessage': 'unable_to_create_stocks'}: 상품 옵션 정보 등록 실패

            History:
                2020-12-29(심원두): 초기 생성
        """
        
        try:
            data = dict()
            print('상품 옵션 등록 서비스1')
            for stock in stocks:
                product_option_code = \
                    str(product_id) + \
                    str(stock['color']).zfill(3) + \
                    str(stock['size']).zfill(3)
                
                data['product_option_code'] = product_option_code
                data['product_id']          = product_id
                data['color_id']            = stock['color']
                data['size_id']             = stock['size']
                data['remain']              = stock['remain']
                data['is_stock_manage']     = stock['isStockManage']
                
                if not data['is_stock_manage']:
                    data['remain'] = 0
                
                print('상품 옵션 등록 서비스2')
                self.create_product_dao.insert_stock(connection, data)

        except KeyError:
            raise KeyError('key_error')

    def create_product_history_service(self, connection, product_id, data):
        """ 상품 이력 정보 등록

            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id
                data       : View 에서 넘겨 받은 상품 정보

            Author: 심원두

            Returns:
                None

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}           : 잘못 입력된 키값

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

        except KeyError:
            raise KeyError('key_error')

    def create_product_sales_volumes_service(self, connection, product_id):
        try:
            print("상품 볼륨 서비스1")
            return self.create_product_dao.insert_product_sales_volumes(connection, product_id)

        except Exception as e:
            raise e

    def main_category_list_service(self, connection):
        try:
            return self.create_product_dao.get_main_category_list(connection)

        except Exception as e:
            raise e

    def get_color_list_service(self, connection):
        try:
            return self.create_product_dao.get_color_list(connection)

        except Exception as e:
            raise e

    def get_size_list_service(self, connection):
        try:
            return self.create_product_dao.get_size_list(connection)

        except Exception as e:
            raise e

    def get_product_origin_types_service(self, connection):
        try:
            return self.create_product_dao.get_product_origin_types(connection)
        
        except Exception as e:
            raise e

    def search_seller_list_service(self, connection, data):
        try:
            if data['seller_name']:
                data['seller_name'] = '%' + data['seller_name'] + '%'

            return self.create_product_dao.search_seller_list(connection, data)

        except Exception as e:
            raise e

    def get_sub_category_list_service(self, connection, data):
        try:
            return self.create_product_dao.get_sub_category_list(connection, data)

        except Exception as e:
            raise e
