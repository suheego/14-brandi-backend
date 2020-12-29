from functools import wraps

from flask import request, g, current_app

import jwt

from utils.custom_exceptions import UnauthorizedUser, InvalidUser

def signin_degorator(func):
    """ 로그인 데코레이터

        Args:
            func            : 로그인 검증 과정이 필요한 타겟 함수
            *args, **kwargs : 타겟 함수가 사용할 파라미터

        Author: 김민구

        Returns:
            func(*args, **kwargs)    : g 객체를 사용해 account_id와 username을 로컬변수로 만들어 타겟 함수에서 사용 가능하게 설정

        Raises:
            401, {'message': 'unauthorized_user', 'errorMessage': 'should_be_signin'}           : 로그인을 안한 유저
            403, {'message': 'invalid_user', 'errorMessage': 'not_authorized_to_perform'}       : 해당 수행 권한이 없음

        History:
            2020-20-29(김민구): 초기 생성
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')

            if not access_token:
                raise UnauthorizedUser('should_be_signin')

            payload = jwt.decode(
                access_token,
                current_app.config['JWT_SECRET_KEY'],
                current_app.config['JWT_ALGORITHM']
            )
            username = payload['username']
            g.username = username
            g.account_id = payload['account_id']

        except jwt.InvalidTokenError:
            raise InvalidUser('not_authorized_to_perform')

        return func(*args, **kwargs)
    return wrapper

