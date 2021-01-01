from functools import wraps

from flask import request, g, current_app

import jwt

from utils.custom_exceptions import UnauthorizedUser, InvalidToken


def signin_decorator(func):
    """ 로그인 데코레이터

        Args:
            func            : 로그인 검증 과정이 필요한 타겟 함수
            *args, **kwargs : 타겟 함수가 사용할 파라미터

        Author: 김민구

        Returns:
            func(*args, **kwargs) : g 객체를 사용해 account_id와 username을 전역변수로 만들어 타겟 함수에서 사용 가능하게 설정

        Raises:
            401, {'message': 'unauthorized_user', 'errorMessage': '로그인이 필요합니다.'} : 로그인을 안한 유저
            403, {'message': 'invalid_token', 'errorMessage': '잘못된 사용자입니다.'}     : 유효하지 않은 토큰

        History:
            2020-12-29(김민구): 초기 생성
            2020-12-31(김민구): 에러 문구 변경

        Notes:
            토큰 유효시간 : 5시간
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')

            if not access_token:
                raise UnauthorizedUser('로그인이 필요합니다.')

            payload = jwt.decode(
                access_token,
                current_app.config['JWT_SECRET_KEY'],
                current_app.config['JWT_ALGORITHM']
            )

            g.username = payload['username']
            g.account_id = payload['account_id']
            g.permission_type_id = payload['permission_type_id']

        except (jwt.InvalidTokenError, jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
            raise InvalidToken('잘못된 사용자입니다.')

        return func(*args, **kwargs)

    return wrapper
