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
        pattern = '^[1-9]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept only number')
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


class DefaultRule(AbstractRule):
    def validate(self, value):
        pattern = '^[0-9A-Za-z가-힣\s.\-_]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept only number, text')
        return value, errors


class RequiredFieldRule(AbstractRule):
    def validate(self, *args):
        errors = []
        if not all([value for value in args]):
            errors.append('required field')

        return args, errors


class RequiredFieldNumberRule(AbstractRule):
    def validate(self, value):
        errors = []
        if not value:
            errors.append('required value')

        return value, errors
