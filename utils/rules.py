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


class DateRule(AbstractRule):
    def validate(self, value):
        pattern = '^([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]))$'
        regex = re.compile(pattern)
        errors = []
        if not regex.match(value):
            errors.append('accept only alphabetic characters')
