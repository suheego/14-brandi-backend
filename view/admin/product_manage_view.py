from flask                   import jsonify, request, json
from flask.views             import MethodView

from utils.connection        import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules             import NumberRule, PageRule, DateRule, DefaultRule
from flask_request_validator import (
    Param,
    GET,
    PATH,
    Enum,
    MaxLength,
    NotEmpty,
    validate_params,
)

class ProductManageSearchView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : MainCategoryListService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 심원두

        History:
            2020-12-31(심원두): 초기 작성
            2021-01-03(심원두): 상품 리스트 검색 기능 구현
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database
    
    @validate_params(
        Param('lookup_start_date', GET, str,  required=False, rules=[DateRule(), NotEmpty()]),
        Param('lookup_end_date',   GET, str,  required=False, rules=[DateRule(), NotEmpty()]),
        Param('seller_name',       GET, str,  required=False, rules=[DefaultRule(), NotEmpty(), MaxLength(20)]),
        Param('product_name',      GET, str,  required=False, rules=[DefaultRule(), NotEmpty(), MaxLength(100)]),
        Param('product_id',        GET, str,  required=False, rules=[NumberRule(), NotEmpty()]),
        Param('product_code',      GET, str,  required=False, rules=[DefaultRule(), NotEmpty(), MaxLength(20)]),
        Param('is_sale',           GET, int,  required=False, rules=[Enum(1, 2)]),
        Param('is_display',        GET, int,  required=False, rules=[Enum(1, 2)]),
        Param('is_discount',       GET, int,  required=False, rules=[Enum(1, 2)]),
        Param('page_number',       GET, int,  required=True,  rules=[PageRule()]),
        Param('limit',             GET, int,  required=True,  rules=[Enum(10, 20, 50)])
    )
    def get(self, *args):
        """GET 메소드: 특정 조건에 해당하는 상품 리스트를 조회한다.
            
            Args:
                'lookup_start_date'       : 조회 시작 기간
                'lookup_end_date'         : 조회 종료 기간
                'seller_name'             : 셀러명
                'product_name'            : 상품명
                'product_id'              : 상품 아이디
                'product_code'            : 상품 코드
                'seller_attribute_type_id : 셀러 속성
                'is_sale'                 : 할인 여부
                'is_display'              : 진열 여부
                'is_discount'             : 할인 여부
                'page_number'             : 페이지 번호
                'limit'                   : 한 화면에 보여줄 상품의 갯수
                
            Author: 심원두
            
            Returns:
                return {"message": "success", "result": result}
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)} : 잘못 입력된 키값
                      
                400, {'message': 'both date field required',
                      'errorMessage': 'both_date_field_required'}: 필수 값 유효성 체크 에러
                      
                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_is_greater_than_end_date'}: 날짜 비교 유효성 체크 에러
                
                400, {'message': 'invalid seller attribute type',
                      'errorMessage': 'invalid_seller_attribute_type'}: 셀러 타입 유효성 체크 에러
            
            History:
                2020-12-31(심원두): 초기생성
                2021-01-03(심원두): 상품 리스트 검색 기능 구현, Login Decorator 구현 예정
        """
        
        try:
            
            data = {
                'lookup_start_date'         : request.args.get('lookup_start_date', None),
                'lookup_end_date'           : request.args.get('lookup_end_date', None),
                'seller_name'               : request.args.get('seller_name', None),
                'product_name'              : request.args.get('product_name', None),
                'product_id'                : request.args.get('product_id', None),
                'product_code'              : request.args.get('product_code', None),
                'seller_attribute_type_ids' : json.loads(request.args.get('seller_attribute_type_id'))
                                              if request.args.get('seller_attribute_type_id')
                                              else None,
                'is_sale'                   : request.args.get('is_sale', None),
                'is_display'                : request.args.get('is_display', None),
                'is_discount'               : request.args.get('is_discount', None),
                'page_number'               : request.args.get('page_number'),
                'limit'                     : request.args.get('limit')
            }
            
            connection = get_connection(self.database)
            result     = self.service.search_product_service(connection, data)
            
            return jsonify({'message': 'success', 'result': result})
        
        except Exception as e:
            raise e
        
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class ProductManageDetailView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : ProductManageDetailView 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 심원두

        History:
            2021-01-02(심원두): 초기 작성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database
    
    @validate_params(
        Param('product_code', PATH, str, required=True, rules=[NotEmpty(), MaxLength(20)]),
    )
    def get(self, *args):
        """GET 메소드: 상품 코드에 해당하는 상품 정보를 불러온다.

            Args:
                'product_code' : 상품 코드

            Author: 심원두

            Returns:
                return {"message": "success", "result": result}
            
            Raises:
                500, {'message': 'product does not exist',
                      'errorMessage': 'product_does_not_exist'} : 상품 정보 취득 실패
                      
                500, {'message': 'product image not exist',
                      'errorMessage': 'product_image_not_exist'}: 상품 이미지 정보 취득 실패
                      
                500, {'message': 'stock info not exist',
                      'errorMessage': 'stock_does_not_exist'}: 옵션 정보 취득 실패
            
            History:
                2021-01-02(심원두): 초기 작성
        """
        
        try:
            data = {
                'product_code' : request.view_args['product_code']
            }
            
            connection = get_connection(self.database)
            result     = self.service.detail_product_service(connection, data)
            
            return jsonify({'message': 'success', 'result': result})
        
        except Exception as e:
            raise e
        
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
