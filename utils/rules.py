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
        print(value)
        pattern = '^[a-zA-Z0-9]{6,20}$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('username_is_not_valid')
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


class EmailRule(AbstractRule):
    def validate(self, value):
        pattern = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('email_is_not_valid')
        return value, errors
