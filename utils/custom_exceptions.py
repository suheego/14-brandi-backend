"""사용자 제작 예외 처리
앱 관련 사용자 제작 예외처리는 모두 이곳에 Exception 클래스를 상속받아 작성한다.
작성한 사용제 제작 예외 처리는 error_handler.py 에서 사용된다.
기본적인 사용 예시:
class IamException(Exception):
        def __init__(self, error_message):
        self.status_code = 400
        self.message = 'your message goes here'
        self.error_message = error_message
        super().__init__(self.status_code, self.message, self.error_message)
"""

# don't touch
class CustomUserError(Exception):
    def __init__(self, status_code, message, error_message):
        self.status_code = status_code
        self.message = message
        self.error_message = error_message


#-----------------------------------------------------------------------------------------------------------------------


class InvalidUserId(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'id_must_be_integer'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UserAlreadyExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 403
        message = "user_already_exist"
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UserUpdateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'user_update_denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UserCreateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'user_create_denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UserNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 404
        message = 'user_not_exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class TokenCreateDenied(CustomUserError):
    """ 토큰 생성 실패 에러

    Author: 김민구

    History:
        2020-12-29(김민구): 초기생성
    """
    def __init__(self, error_message):
        status_code = 500
        message = 'token_create_denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class InvalidUser(CustomUserError):
    """ 적합하지 않은 사용자 에러

    Author: 김민구

    History:
        2020-12-29(김민구): 초기생성
    """
    def __init__(self, error_message):
        status_code = 403
        message = 'invalid_user'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class InvalidToken(CustomUserError):
    """ 토큰 검증 에러

    Author: 김민구

    History:
        2020-12-29(김민구): 초기생성
    """
    def __init__(self, error_message):
        status_code = 403
        message = 'invalid_token'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class TokenCreateDenied(CustomUserError):
    """ 토큰 생성 에러

    Author: 김민구

    History:
        2020-12-29(김민구): 초기생성
    """
    def __init__(self, error_message):
        status_code = 500
        message = 'token_create_denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UnauthorizedUser(CustomUserError):
    """ 인증이 필요한 사용자 에러

    Author: 김민구

    History:
        2020-12-28(김민구): 초기생성
    """
    def __init__(self, error_message):
        status_code = 401
        message = 'unauthorized_user'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DatabaseCloseFail(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = "database_close_fail"
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DatabaseError(CustomUserError):
    """ 데이터 베이스 에러

    Author: 김민구

    History:
        2020-12-28(김민구): 초기생성
    """
    def __init__(self, error_message):
        status_code = 500
        message = "database_error"
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DestinationNotExist(CustomUserError):
    """ 배송지 조회 불가

    Author: 김기용

    History:
        2020-12-28(김기용): 초기생성
    """
    def __init__(self, error_message):
        status_code = 401
        message = 'destination_does_not_exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)
       

class DestinationCreateDenied(CustomUserError):
    """ 배송지 생성 거절

    Author: 김기용

    History:
        2020-12-28(김기용): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'destination_creatation_denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)

        
class SellerNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'seller not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class SellerUpdateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'user update denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)

class SellerNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'seller not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class SellerUpdateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'user update denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class RequiredFieldException(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'required field is blank'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CompareQuantityCheck(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'compare quantity field check error'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ComparePriceCheck(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'compare price field check error'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductCreateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'product create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductCodeUpdatedDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'product code update denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductImageCreateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'product image create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class StockCreateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'stock create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductHistoryCreateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'product history create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductSalesVolumeCreateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'product sales volume create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductOriginTypesNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'fail to get product origin types'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class SizeNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'fail to get size list'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ColorNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'fail to get color list'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class MainCategoryNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'fail to get main category list'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class SubCategoryNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'fail to get sub category list'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class NotValidFileException(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'invalid file'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class FileSizeException(CustomUserError):
    def __init__(self, error_message):
        status_code = 413
        message = 'file size too large'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class FileScaleException(CustomUserError):
    def __init__(self, error_message):
        status_code = 413
        message = 'file scale too small, 640 * 720 at least'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class FileExtensionException(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'only allowed jpg type'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class FileUploadFailException(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'image_file_upload_to_amazon_fail'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class NotUser(CustomUserError):
    """ 유저가 아님

    Author: 김기용

    History:
        2020-12-28(김기용): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'not_a_user'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class AccountNotExist(CustomUserError):
    """ 계정정보없음

    Author: 김기용

    History:
        2020-12-28(김기용): 초기생성
    """
    def __init__(self, error_message):
        status_code = 401
        message = 'account_does_not_exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CartItemNotExist(CustomUserError):
    """ 장바구니 상품 조회 실패 

    Author: 고수희

    History:
        2020-12-28(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'cart items not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CartItemCreateDenied(CustomUserError):
    """ 장바구니 상품 추가 실패

    Author: 고수희

    History:
        2020-12-28(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'cart item create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DataLimitExceeded(CustomUserError):
    """ 데이터 제한 초과

    Author: 김기용

    History:
        2020-12-28(김기용): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'data_limit_reached'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CustomerPermissionDenied(CustomUserError):
    """ 일반 유저 권한이 아님

    Author: 고수희

    History:
        2020-12-28(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'customer permissions denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductNotExist(CustomUserError):
    """ 상품이 존재하지 않음

    Author: 고수희

    History:
        2020-12-30(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'product does not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DeleteDenied(CustomUserError):
    """ 논리 삭제 거부

    Author: 김기용

    History:
        2020-12-30(김기용): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'invalid_delete_command_access'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DateMissingOne(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'date inputs should be start_date and end_date'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UpdateDenied(CustomUserError):
    """ 수정 거부

    Author: 김기용

    History:
        2020-12-30(김기용): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'unable_to_update'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class EventSearchTwoInput(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'event search inputs must be only one'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DateMissingOne(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'date inputs should be start_date and end_date'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class SearchTwoInput(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'search inputs must be only one'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class EventDoesNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 404
        message = 'event not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class OrderFilterNotExist(CustomUserError):
    """ 필터 조건 없음

        Author: 김민서

        History:
            2020-12-31(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'must_be_date_inputs_or_filter_inputs'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class OrderDoesNotExist(CustomUserError):
    """ 주문 리스트 없음

        Author: 김민서

        History:
            2020-12-31(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'order does not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CategoryMenuDoesNotMatch(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'menu id does not match with category id'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CheckoutDenied(CustomUserError):
    """ 상품 결제 거부

    Author: 고수희

    History:
        2020-12-31(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'unable_to_checkout'
        error_message = error_message
        super().__init__(status_code, message, error_message)

        
class NoPermission(CustomUserError):
    """ 권한 없음

        Author: 김민서

        History:
            2020-12-31(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 403
        message = 'no_permission'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class NotAllowedStatus(CustomUserError):
    """ 주문 상태 변경 가능 상태가 아님

        Author: 김민서

        History:
            2021-01-01(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'now_order_status_is_not_allowed_to_update_status'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DoesNotOrderDetail(CustomUserError):
    """ 주문 상세 정보 없음

        Author: 김민서

        History:
            2021-01-01(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'does_not_exist_order_detail'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class OrderCreateDenied(CustomUserError):
    """ 결제 추가 실패

        Author: 고수희

        History:
            2020-12-31(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 404
        message = 'order create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DeliveryMemoCreateDenied(CustomUserError):
    """ 배송 메모 추가 실패

        Author: 고수희

        History:
            2020-12-31(고수희): 초기생성
    """

    def __init__(self, error_message):
        status_code = 404
        message = 'delivery memo create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)

        
class OrderItemCreateDenied(CustomUserError):
    """ 결제 상품 정보 추가 실패

        Author: 고수희

        History:
            2020-12-31(고수희): 초기생성
    """

    def __init__(self, error_message):
        status_code = 404
        message = 'order item create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ServerError(CustomUserError):
    """ 서버 에러 출력

        Author: 고수희

        History:
            2021-01-01(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 500
        message = "server_error"
        error_message = error_message
        super().__init__(status_code, message, error_message)

        
class OrderNotExist(CustomUserError):
    """ 상품 조회 실패
    
        Author: 고수희

        History:
            2021-01-01(고수희): 초기생성
    """
    def __init__(self, error_message):
      status_code = 404
      message = "order does not exist"
      error_message = error_message
      super().__init__(status_code, message, error_message)

      
class SellerNotExist(CustomUserError):
    """ 셀러 조회 실패

        Author: 고수희

        History:
            2021-01-01(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 404
        message = 'seller does not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DataManipulationFail(CustomUserError):
    """ 데이터 조작 실패


        Author: 김민구

        History:
            2021-01-02(김민구): 초기생성
    """
    def __init__(self, error_message):
        status_code = 500
        message = 'data_manipulation_fail'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class AlreadyExistBookmark(CustomUserError):
    """ 북마크 이미 존재

        해당 북마크가 이미 존재할 때 발생

        Author: 김민구

        History:
            2021-01-02(김민구): 초기생성
    """

    def __init__(self, error_message):
        status_code = 400
        message = 'already_exist_bookmark'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class NotExistBookmark(CustomUserError):
    """ 북마크가 존재하지 않음

        해당 북마크가 존재하지 않을 때 발생

        Author: 김민구

        History:
            2021-01-02(김민구): 초기생성
    """

    def __init__(self, error_message):
        status_code = 404
        message = 'not_exist_bookmark'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class OrderHistoryCreateDenied(CustomUserError):
    """ 상품 정보 이력 추가 실패
    
        Author: 고수희

        History:
        2020-01-02(고수희): 초기생성
    """

    def __init__(self, error_message):
        status_code = 404
        message = 'order history create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class SellerCategoryNotExist(CustomUserError):
    """ 셀러 카테고리 조회 실패
    
        Author: 

        History:
        2021-01-03(고수희): 초기생성
    """
    def __init__(self, error_message):
        status_code = 404
        message = 'seller category not exist'
        error_massage = error_massage
        super().__init__(status_code, message, error_massage)

        
class CategoryDoesNotExist(CustomUserError):
    def __init__(self, error_massage):
        status_code = 400
        message = 'category not exist'
        error_massage = error_massage
        super().__init__(status_code, message, error_massage)


class FilterDoesNotMatch(CustomUserError):
    def __init__(self, error_massage):
        status_code = 400
        message = 'filter does not match'
        error_massage = error_massage
        super().__init__(status_code, message, error_massage)


class SearchFilterRequired(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'filter must be at least one'
        super().__init__(status_code, message, error_massage)


class DateInputDoesNotExist(CustomUserError):
    """날짜 조건 없음

        Author: 김민서

        History:
            2020-12-31(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'must_be_other_date_input'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class InputDoesNotExist(CustomUserError):
    """ 수정 정보 존재하지 않음

        Author: 김민서

        History:
            2021-01-02(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'input_does_not_exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UnableUpdateAddress(CustomUserError):
    """ 수정할 주소 정보 부족

        Author: 김민서

        History:
            2021-01-02(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'one_of_address_inputs_does_not_exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UnableToUpdate(CustomUserError):
    """ 수정 불가

        Author: 김민서

        History:
            2021-01-02(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'unable_to_update'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class DeniedUpdate(CustomUserError):
    """ 수정 실패

        Author: 김민서

        History:
            2021-01-02(김민서): 초기생성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'denied_to_update'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class EventKindDoesNotMatch(CustomUserError):
    """ 기획전 종류가 버튼형이 아닌데 버튼데이터를 받은경우

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'Event kind does not match'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ButtonsMinimumCount(CustomUserError):
    """ 기획전 종류가 버튼형일때 버튼이 두개이상

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'at least two buttons should be created'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class StartAndEndDateContext(CustomUserError):
    """ 시작날짜가 종료날짜보다 미래일 때

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'start date and end date context error'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ImageIsRequired(CustomUserError):
    """ 이미지가 필요함

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """
    def __init__(self, error_message):
        status_code = 400
        message = 'image files are required'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CreateEventDenied(CustomUserError):
    """ 이벤트 생성 실패

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """

    def __init__(self, error_message):
        status_code = 400
        message = 'unable to create event'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CreateButtunDenied(CustomUserError):
    """ 이벤트 버튼 생성 실패

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """

    def __init__(self, error_message):
        status_code = 400
        message = 'unable to create event button'
        error_message = error_message
        super().__init__(status_code, message, error_message)

        
class DateCompareException(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'start date is greater than end date'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductImageNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'product image not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class StockNotNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'stock info not exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class LookUpDateFieldRequiredCheck(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'both date field required'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class SellerAttributeTypeException(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'invalid seller attribute type'
        error_message = error_message
        super().__init__(status_code, message, error_message)

        
class ProductSalesRateCreateDenied(CustomUserError):
    """ 상품 판매량 추가 실패

        Author: 고수희

        History:
            2021-01-02(고수희): 초기생성
    """

    def __init__(self, error_message):
        status_code = 404
        message = 'order history create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)

        
class ProductRemainUpdateDenied(CustomUserError):
    """ 상품 재고 업데이트 실패

        Author: 고수희

        History:
            2021-01-02(고수희): 초기생성
    """

    def __init__(self, error_message):
        status_code = 404
        message = 'product remain update denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class CustomerInformationCreateDenied(CustomUserError):
    """ 주문자 정보 추가 실패

        Author: 고수희

        History:
            2021-01-02(고수희): 초기생성
    """

    def __init__(self, error_message):
        status_code = 404
        message = 'customer information create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ProductButtonNameRequired(CustomUserError):
    """ 기획전 종류가 버튼인데 버튼이름 키,값이 상품데이터에 없을 때

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """

    def __init__(self, error_message):
        status_code = 400
        message = 'button name is required in each product'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class InsertProductIntoButtonDenied(CustomUserError):
    """ 버튼에 상품추가 실패

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """

    def __init__(self, error_message):
        status_code = 400
        message = 'unable to insert product into button'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class InsertProductIntoEventDenied(CustomUserError):
    """ 버튼에 상품추가 실패

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """

    def __init__(self, error_message):
        status_code = 400
        message = 'unable to insert product into event'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class ButtonProductDoesNotMatch(CustomUserError):
    """ 기획전 종류가 버튼형이고 상품추가할 객체가 있지만 상품과 매치된 버튼이 단 하나도 없음

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """

    def __init__(self, error_message):
        status_code = 400
        message = 'although there are product and button objects, no buttons are matched'
        error_message = error_message
        super().__init__(status_code, message, error_message)
