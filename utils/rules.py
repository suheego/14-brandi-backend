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
            errors.append('오직 숫자만 받는다.')
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


class SellerInfoRule(AbstractRule):
    def validate(self, value):
        pattern = '^[0-9]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept only number')
        return value, errors


class DefaultRule(AbstractRule):
    def validate(self, value):
        pattern = '^[a-zA-Z가-힝0-9+-_.]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('accept only number, text')
        return value, errors


class UsernameRule(AbstractRule):
    """ 비밀번호 규칙

    6~20 글자의 대소문자,숫자만 허용한다.

    Author: 김민구

    History:
        2020-12-28(김민구): 초기생성
    """

    def validate(self, value):
        pattern = '^[a-zA-Z0-9]{6,20}$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('please_enter_6-20_letters_or_numbers')
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
    """ 비밀번호 규칙

    8~20 자리 숫자, 대소문자, 특수문자를 모두 넣어야 허용한다.

    Author: 김민구

    History:
        2020-12-28(김민구): 초기생성
    """

    def validate(self, value):
        pattern = '^.*(?=.{8,20})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)(?=.*[!@#£$%^&*()_+={}\-?:~\[\]])[a-zA-Z0-9!@#£$%^&*()_+={}\-?:~\[\]]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('8~20_characters_including_numbers_uppercase_letters_lowercase_letters_special_characters')
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
    """ 이메일 규칙

    @ 앞은 이메일의 아이디에 해당하며 대소문자, 숫자, 특수문자(-_)를 사용할 수 있다.
    @ 다음은 도메인이며 대소문자, 숫자로 이루어져 있다.
    . 다음은 최상위 도메인이며 대소문자 숫자로 이루어진다.

    Author: 김민구

    History:
        2020-12-28(김민구): 초기생성
    """

    def validate(self, value):
        pattern = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        errors = []
        if not result:
            errors.append('this_email_is_incorrect')
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
        bool_set = ['0', '1']
        errors = []
        if value not in bool_set:
            errors.append('0 과 1 값만 받는다.')
        return value, errors


class EventStatusRule(AbstractRule):
    def validate(self, value):
        status_set = ('progress', 'wait', 'end')
        errors = []
        if value not in status_set:
            errors.append('event status must be one of progress, wait and end')
        return value, errors


class BooleanRule(AbstractRule):
    def validate(self, value):
        exposure_set = (0, 1)
        errors = []
        if value not in exposure_set:
            errors.append('boolean field value should be 0 or 1')
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
            errors.append('date format should be YYYY-MM-DD')
        return value, errors



class DateTimeRule(AbstractRule):
    """ DateTime 형식 벨리데이터 (YYYY-MM-DD hh:mm)

        Author: 강두연

        History:
            2021-01-02(강두연): 작성
    """
    def validate(self, value):
        from datetime import datetime
        errors = []
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            errors.append('datetime format should be YYYY-MM-DD hh:mm')
        finally:
            return value, errors

          
class SecondDateTimeRule(AbstractRule):
    """ 날짜 시간 형식 벨리데이터 (YYYY-MM-DD HH:MM:SS)

        Author: 김민서

        History:
            2020-12-29(김민서): 날짜 시간 형식 벨리데이터 역할 규칙 작성
    """
    def validate(self, value):
        pattern = '^([0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2})$'
        regex = re.compile(pattern)
        errors = []
        if not regex.match(value):
            errors.append('datetime must be "YYYY-MM-DD HH:MM:SS"')
        return value, errors


class ProductMenuRule(AbstractRule):
    """ 상품 분류 메뉴 규칙 (트렌드, 브랜드, 뷰티) id는 (4, 5, 6)

        Author: 강두연

        History:
            2020-12-31(강두연): 작성
    """
    def validate(self, value):
        menu_set = (4, 5, 6)
        errors = []
        if value not in menu_set:
            errors.append('accept only id of trend, brand, beauty')
        return value, errors


class CategoryFilterRule(AbstractRule):
    """ 카테고리 불러올 때 필터 규칙

    """
    def validate(self, value):
        filter_set = ('menu', 'both', 'none')
        errors = []
        if value not in filter_set:
            errors.append('accept only (menu, both, none) as a filter value')
        return value, errors


class PageRule(AbstractRule):
    """ 페이지네이션 page는 1이상

    """
    def validate(self, value):
        errors = []
        if value <= 0:
            errors.append('page cannot be less than 1')
        return value, errors


