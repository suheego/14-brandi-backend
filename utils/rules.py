"""사용자 제작 규칙을 정의한다.

request 를 통해 받은 Parameter 값을 이곳에 정의된 규칙과 비교해 에러 메세지를 처리해준다.

기본적인 사용 예시:

class CustomRule(AbstractRule):
    def validate(self, value:str) -> Tuple[str, list[str]]:
        ...
        return value, errors

"""

import re
from flask_request_validator import AbstractRule


class NumberRule(AbstractRule):
    def validate(self, value):
        pattern = '^[0-9]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept_only_number')
        return value, errors


class AlphabeticRule(AbstractRule):
    def validate(self, value):
        pattern = '^[A-Za-z]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept only alphabetic characters')
        return value, errors


class GenderRule(AbstractRule):
    def validate(self, value):
        gender_set = ['male', 'female']
        errors = []
        if value not in gender_set:
            errors.append('accept only male and female value')
        return value, errors


class UsernameRule(AbstractRule):
    def validate(self, value):
        pattern = '^[a-zA-Z0-9]{6,20}$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('username_is_not_valid')
        return value, errors

      
class PhoneRule(AbstractRule):
    """ 휴대폰 자리수 규칙

    10~11 자리 숫자를 허용한다.

    Author: 김기용

    History:
        2020-12-28(김기용): 초기생성
    """
    def validate(self, value):
        pattern = '^[0-9]{10,11}$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept only 10~11 digit numbers')
        return value, errors


class PasswordRule(AbstractRule):
    def validate(self, value):
        pattern = '^.*(?=.{8,18})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)(?=.*[!@#£$%^&*()_+={}\-?:~\[\]])[a-zA-Z0-9!@#£$%^&*()_+={}\-?:~\[\]]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('password_is_not_valid')
        return value, errors


class PostalCodeRule(AbstractRule):
    """ 우편번호 자리수 규칙

    8 자리 숫자만 허용한다.

    Author: 김기용

    History:
        2020-12-28(김기용): 초기생성
    """
    def validate(self, value):
        pattern = '^[0-9]{8}$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept only 8 digit numbers')
        return value, errors


class EmailRule(AbstractRule):
    def validate(self, value):
        pattern = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('email_is_not_valid')
        return value, errors


class DecimalRule(AbstractRule):
    def validate(self, value):
        pattern = '^\d*\.?\d*$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept only decimal value')
        return value, errors


class IsDeleteRule(AbstractRule):
    """ 논리 삭제 규칙

    0, 1 만 허용한다.

    Author: 김기용

    History:
        2020-12-28(김기용): 초기생성
    """
    def validate(self, value):
        gender_set = ['0', '1']
        errors = []
        if value not in gender_set:
            errors.append('accept only 0 and 1 value')

class EventStatusRule(AbstractRule):
    def validate(self, value):
        status_set = ('progress', 'wait', 'end')
        errors = []
        if value not in status_set:
            errors.append('event status must be one of progress, wait and end')
        return value, errors


class EventExposureRule(AbstractRule):
    def validate(self, value):
        exposure_set = (0, 1)
        errors = []
        if value not in exposure_set:
            errors.append('event exposure value should be 0 or 1')
        return value, errors

class OrderStatusRule(AbstractRule):
    def validate(self, value):
        status_set = [1, 2, 3, 8]
        errors = []
        if value not in status_set:
            errors.append('order status must be one of 1, 2, 3, 8')
        return value, errors


class DateRule(AbstractRule):
    """ 날짜 형식 벨리데이터 (YYYY-MM-DD)

        Author: 강두연

        History:
            2020-12-29(강두연): 날짜 형식 벨리데이터 역할 규칙 작성
    """
    def validate(self, value):
        pattern = '^([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]))$'
        regex = re.compile(pattern)
        errors = []
        if not regex.match(value):
            errors.append('accept only alphabetic characters')
        return value, errors
