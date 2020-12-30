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
        message = 'user_already_exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UserUpdateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'user update denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UserCreateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'user create denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class UserNotExist(CustomUserError):
    def __init__(self, error_message):
        status_code = 404
        message = 'user_not_exist'
        error_message = error_message
        super().__init__(status_code, message, error_message)


class InvalidUser(CustomUserError):
    def __init__(self, error_message):
        status_code = 403
        message = 'invalid_user'
        error_message = error_message
        super().__init__(status_code, message, error_message)

class InvalidToken(CustomUserError):
    def __init__(self, error_message):
        status_code = 403
        message = 'invalid_token'
        error_message = error_message
        super().__init__(status_code, message, error_message)

class TokenCreateDenied(CustomUserError):
    def __init__(self, error_message):
        status_code = 500
        message = 'token_create_denied'
        error_message = error_message
        super().__init__(status_code, message, error_message)

class UnauthorizedUser(CustomUserError):
    def __init__(self, error_message):
        status_code = 401
        message = 'unauthorized_user'
        error_message = error_message
        super().__init__(status_code, message, error_message)

class DatabaseCloseFail(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'database connection fail'
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

# S - 상품 등록 관련 Exception Class ===============================================================
class RequiredFieldException(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'required field is blank'
        error_message = error_message
        super().__init__(status_code, message, error_message)

class CorrelationCheckException(CustomUserError):
    def __init__(self, error_message):
        status_code = 400
        message = 'correlation check fail'
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

# E - 상품 등록 관련 Exception Class ===============================================================

