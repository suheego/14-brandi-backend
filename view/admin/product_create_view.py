import traceback

from flask                          import jsonify, request, json, g
from flask.views                    import MethodView
from flask_request_validator.rules  import NotEmpty

from utils.connection               import get_connection
from utils.decorator                import signin_decorator
from utils.custom_exceptions        import DatabaseCloseFail
from utils.rules                    import NumberRule

from flask_request_validator import (
    Param,
    FORM,
    GET,
    MaxLength,
    Enum,
    validate_params
)


class MainCategoriesListView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : MainCategoryListService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 심원두

        History:
            2020-12-30(심원두): 초기 작성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database
    
    @signin_decorator()
    def get(self, *args):
        """GET 메소드: 상품 정보 등록에 필요한 메인 카테고리 리스트 취득

            Args: None

            Author: 심원두

            Returns:
                result - 메인 카테고리 리스트

            Raises:
                500, {'message': 'fail to get main category list',
                      'errorMessage': 'fail_to_get_main_category_list'}: 메인 카테고리 정보 취득 실패

            History:
                2020-12-30(심원두): 초기생성
        """
        try:
            connection = get_connection(self.database)
            result     = self.service.main_category_list_service(connection)
            
            return jsonify({'message': 'success', 'result': result})
        
        except KeyError as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class CreateProductView(MethodView):
    """ Presentation Layer
        
        Attributes:
            service  : CreateProductService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        
        Author: 심원두
        
        History:
            2020-12-29(심원두): 초기 생성. products insert, product_code updated, product_histories 생성 기능 작성
            2020-12-30(심원두): 각 Param rules 추가, stock insert 기능 작성.
            2020-01-03(심원두): 상품 등록 Param rules 추가
    """
    
    def __init__(self, service, database):
        self.service = service
        self.database = database
    
    @signin_decorator()
    @validate_params(
        Param('seller_name',      GET, str, required=False, rules=[MaxLength(20)]),
        Param('main_category_id', GET, str, required=False, rules=[NumberRule()])
    )
    def get(self, *args):
        """POST 메소드: 상품 정보 등록 초기 화면
            
            Args:
                'seller_name'      : 사용자가 입력한 셀러명
                'main_category_id' : 사용자가 선택한 메인 카테고리 아이디
            
            Author: 심원두
            
            Returns:
                return {"message": "success", "result": [{}]}
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값
                      
                500, {'message': 'fail to get sub category list',
                      'errorMessage': 'fail_to_get_sub_category_list'}: 색상 정보 취득 실패
                
                500, {'message': 'fail to get product origin types',
                      'errorMessage': 'fail_to_get_product_origin_types'} : 원산지 정보 취득 실패
                
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패
                
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패
            
            History:
                2020-12-30(심원두): 초기생성
                2021-01-06(심원두): 로그인 데코레이터 처리 추가. 관리자일 경우에만 셀러 검색 허용하도록 수정
        """
        
        try:
            data = {
                'seller_name'      : request.args.get('seller_name', None),
                'main_category_id' : request.args.get('main_category_id', None)
            }
            
            connection = get_connection(self.database)
            
            if data['seller_name'] and g.permission_type_id == 1:
                sellers = self.service.search_seller_list_service(
                    connection,
                    data
                )
            
                return jsonify({'message': 'success', 'result': sellers})
            
            if data['main_category_id']:
                sub_categories = self.service.get_sub_category_list_service(
                    connection,
                    data
                )
                
                return jsonify({'message': 'success', 'result': sub_categories})
            
            result = dict()
            
            result['product_origin_types'] = \
                self.service.get_product_origin_types_service(
                    connection
            )
            
            result['color_list'] = \
                self.service.get_color_list_service(
                    connection
                )
            
            result['size_list'] =  \
                self.service.get_size_list_service(
                    connection
                )
            
            return jsonify({'message': 'success', 'result': result})
        
        except KeyError as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
        
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
    
    @signin_decorator()
    @validate_params(
        Param('seller_id',              FORM, str,  required=True,  rules=[NumberRule()]),
        Param('is_sale',                FORM, int,  required=True,  rules=[Enum(0, 1)]),
        Param('is_display',             FORM, int,  required=True,  rules=[Enum(0, 1)]),
        Param('main_category_id',       FORM, str,  required=True,  rules=[NumberRule()]),
        Param('sub_category_id',        FORM, str,  required=True,  rules=[NumberRule()]),
        Param('is_product_notice',      FORM, int,  required=True,  rules=[Enum(0, 1)]),
        Param('manufacturer',           FORM, str,  required=False, rules=[MaxLength(30)]),
        Param('manufacturing_date',     FORM, str,  required=False),
        Param('product_origin_type_id', FORM, str,  required=False),
        Param('product_name',           FORM, str,  required=True,  rules=[NotEmpty(), MaxLength(100)]),
        Param('description',            FORM, str,  required=False, rules=[MaxLength(200)]),
        Param('detail_information',     FORM, str,  required=True,  rules=[NotEmpty()]),
        Param('options',                FORM, list, required=True),
        Param('minimum_quantity',       FORM, str,  required=False, rules=[NumberRule()]),
        Param('maximum_quantity',       FORM, str,  required=False, rules=[NumberRule()]),
        Param('origin_price',           FORM, str,  required=True,  rules=[NumberRule()]),
        Param('discount_rate',          FORM, str,  required=True,  rules=[NumberRule()]),
        Param('discounted_price',       FORM, str,  required=True,  rules=[NumberRule()]),
        Param('discount_start_date',    FORM, str,  required=False),
        Param('discount_end_date',      FORM, str,  required=False)
    )
    def post(self, *args):
        """ POST 메소드: 상품 정보 등록
            
            Args:
            - 사용자 입력 값(상품 이미지 최대 5개) : image_files
            - 사용자 입력 값(옵션 정보 리스트)    : options
            - 사용자 입력 값
            Form-Data: (
                'seller_id'
                'account_id',
                'is_sale',
                'is_display',
                'main_category_id',
                'sub_category_id',
                'is_product_notice',
                'manufacturer',
                'manufacturing_date',
                'product_origin_type_id',
                'product_name',
                'description',
                'detail_information',
                'options',
                'minimum_quantity',
                'maximum_quantity',
                'origin_price',
                'discount_rate',
                'discounted_price',
                'discount_start_date',
                'discount_end_date',
            )
            
            Author: 심원두
            
            Returns:
                200, {'message': 'success'}                                                   : 상품 정보 등록 성공
            
            Raises:
                400, {'message': 'key_error',
                      'errorMessage': 'key_error_' + format(e)}                               : 잘못 입력된 키값
                
                400, {'message': 'required field is blank',
                      'errorMessage': 'required_manufacture_information'}                     : 제조 정보 필드 없음
                
                400, {'message': 'required field is blank',
                      'errorMessage': 'required_discount_start_or_end_date'}                  : 필수 입력 항목 없음
                
                400, {'message': 'compare quantity field check error',
                      'errorMessage': 'minimum_quantity_cannot_greater_than_maximum_quantity'}: 최소 구매 수량이 최대 보다 큼
                
                400, {'message': 'compare price field check error',
                      'errorMessage': 'discounted_price_cannot_greater_than_origin_price'}    : 할인가가 판매가 보다 큼

                400, {'message': 'compare price field check error',
                      'errorMessage': 'wrong_discounted_price'}                               : 판매가와 할인가 일치하지 않음
                
                400, {'message': 'compare price field check error',
                      'errorMessage': 'required_discount_start_or_end_date'}                  : 할인 시작, 종료 일자 필드 없음
                
                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_cannot_greater_than_end_date'}              : 할인 시작일이 종료일 보다 큼
                
                400, {'message': 'compare price field check error',
                      'errorMessage': 'discounted_price_have_to_same_with_origin_price'}      : 할인가, 판매가 불일치(할인율 0)
                
                413, {'message': 'invalid file',
                      'errorMessage': 'invalid_file'}                                         : 파일 이름이 공백, 혹은 파일을 정상적으로 받지 못함
                
                413, {'message': 'file size too large',
                      'errorMessage': 'file_size_too_large'}                                  : 파일 사이즈 정책 위반 (4메가 이상인 경우)
                
                413, {'message': 'file scale too small, 640 * 720 at least',
                      'errorMessage': 'file_scale_at_least_640*720'}                          : 파일 스케일 정책 위반 (680*720 미만인 경우)

                413, {'message': 'only allowed jpg type',
                      'errorMessage': 'only_allowed_jpg_type'}                                : 파일 확장자 정책 위반 (JPG, JPEG 아닌 경우)
                
                500, {'message': 'image_file_upload_to_amazon_fail',
                      'errorMessage': 'image_file_upload_fail'}                               : 이미지 업로드 실패
                
                500, {'message': 'product create denied',
                      'errorMessage': 'unable_to_create_product'}                             : 상품 정보 등록 실패
                
                500, {'message': 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'}                        : 상품 코드 갱신 실패
                
                500, {'message': 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'}                        : 상품 코드 갱신 실패
                
                500, {'message': 'product image create denied',
                      'errorMessage': 'unable_to_create_product_image'}                       : 상품 이미지 등록 실패
                
                500, {'message': 'stock create denied',
                      'errorMessage': 'unable_to_create_stocks'}                              : 상품 옵션 정보 등록 실패
                
                500, {'message': 'product history create denied',
                      'errorMessage': 'unable_to_create_product_history'}                     : 상품 이력 등록 실패
                
                500, {'message': 'bookmark volumes create denied',
                      'errorMessage': 'unable_to_create_bookmark_volumes'}                    : 북마크 초기 등록 실패
                
                500, {'message': 'database_connection_fail',
                      'errorMessage': 'database_close_fail'}                                  : 커넥션 종료 실패

                500, {'message': 'database_error',
                      'errorMessage': 'database_error_' + format(e)}                          : 데이터베이스 에러

                500, {'message': 'internal_server_error',
                      'errorMessage': format(e)})                                             : 서버 에러
            
            History:
                2020-12-29(심원두): 초기 생성
                2021-01-03(심원두): 파라미터 유효성 검사 추가 Enum(), NotEmpty()
                2021-01-05(심원두): -이미지 저장 처리 순서를 3번째에서 가장 마지막으로 내림. 테이블 인서트 처리에 문제가 있을 경우,
                                    S3에 올라간 이미지는 롤백을 할 수 없는 이슈 반영.
                                   -북마크 테이블 초기 등록 처리 추가.
        """
        
        try:
            data = {
                'seller_id'              : request.form.get('seller_id'),
                'account_id'             : g.account_id,
                'is_sale'                : request.form.get('is_sale'),
                'is_display'             : request.form.get('is_display'),
                'main_category_id'       : request.form.get('main_category_id'),
                'sub_category_id'        : request.form.get('sub_category_id'),
                'is_product_notice'      : request.form.get('is_product_notice'),
                'manufacturer'           : request.form.get('manufacturer', None),
                'manufacturing_date'     : request.form.get('manufacturing_date', None),
                'product_origin_type_id' : request.form.get('product_origin_type_id', None),
                'product_name'           : request.form.get('product_name'),
                'description'            : request.form.get('description'),
                'detail_information'     : request.form.get('detail_information'),
                'minimum_quantity'       : request.form.get('minimum_quantity'),
                'maximum_quantity'       : request.form.get('maximum_quantity'),
                'origin_price'           : request.form.get('origin_price'),
                'discount_rate'          : request.form.get('discount_rate'),
                'discounted_price'       : request.form.get('discounted_price'),
                'discount_start_date'    : request.form.get('discount_start_date', None),
                'discount_end_date'      : request.form.get('discount_end_date', None)
            }
            
            connection     = get_connection(self.database)
            product_images = request.files.getlist("image_files")
            stocks         = json.loads(request.form.get('options'))
            
            product_id = self.service.create_product_service(
                connection,
                data
            )
            
            product_code = self.service.update_product_code_service(
                connection,
                product_id
            )
            
            self.service.create_stock_service(
                connection,
                product_id,
                stocks
            )
            
            self.service.create_product_history_service(
                connection,
                product_id,
                data
            )
            
            self.service.create_product_sales_volumes_service(
                connection,
                product_id
            )
            
            self.service.create_bookmark_volumes_service(
                connection,
                product_id
            )
            
            self.service.create_product_images_service(
                connection,
                data['seller_id'],
                product_id,
                product_code,
                product_images
            )
            
            connection.commit()
            
            return jsonify({'message': 'success'}), 200
            
        except KeyError as e:
            traceback.print_exc()
            connection.rollback()
            raise e
            
        except Exception as e:
            traceback.print_exc()
            connection.rollback()
            raise e
        
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                traceback.print_exc()
                raise DatabaseCloseFail('database close fail')
