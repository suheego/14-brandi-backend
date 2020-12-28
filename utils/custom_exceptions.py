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
        self.status_code = 400
        self.message = 'user_id must be integer'
        self.error_message = error_message
        super().__init__(self.status_code, self.message, self.error_message)


class UserAlreadyExist(CustomUserError):
    def __init__(self, error_message):
        self.status_code = 400
        self.message = 'user already exist'
        self.error_message = error_message
        super().__init__(self.status_code, self.message, self.error_message)


class UserUpdateDenied(CustomUserError):
    def __init__(self, error_message):
        self.status_code = 400
        self.message = 'user update denied'
        self.error_message = error_message
        super().__init__(self.status_code, self.message, self.error_message)


class UserCreateDenied(CustomUserError):
    def __init__(self, error_message):
        self.status_code = 400
        self.message = 'user create denied'
        self.error_message = error_message
        super().__init__(self.status_code, self.message, self.error_message)


class UserNotExist(CustomUserError):
    def __init__(self, error_message):
        self.status_code = 400
        self.message = 'user not exist'
        self.error_message = error_message

        super().__init__(self.status_code, self.message, self.error_message)


class DatabaseCloseFail(CustomUserError):
    def __init__(self, error_message):
        self.status_code = 400
        self.message = 'database connection fail'
        self.error_message = error_message
        super().__init__(self.status_code, self.message, self.error_message)
