from datetime import datetime, timedelta

import bcrypt
import jwt

from utils.custom_exceptions import UserAlreadyExist, InvalidUser, TokenCreateDenied
from model import UserDao


class UserService:
    """ Business Layer

        Attributes:
            user_dao : UserDao 클래스

        Author: 김민구

        History:
            2020-12-28(김민구): 초기 생성
            2020-12-31(김민구): user_dao를 import 해서 사용하는 방법으로 수정
    """

    def __init__(self, config):
        self.config = config
        self.user_dao = UserDao()

    def sign_up_logic(self, data, connection):
        """ 유저생성

            Args:
                data       : View 에서 넘겨받은 dict 객체
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                None

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)}                          : 잘못 입력된 키값
                403, {'message': 'user_already_exist', 'error_message': '이미 사용중인 [데이터] 입니다.'} : 중복 유저 존재

            History:
                2020-12-28(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
        """

        username_check = self.user_dao.username_exist_check(connection, data)
        email_check = self.user_dao.email_exist_check(connection, data)
        phone_check = self.user_dao.phone_exist_check(connection, data)
        if username_check or email_check or phone_check:
            raise UserAlreadyExist(
                '이미 사용중인 ' +
                ', '.join((' username' * username_check +
                           ' email' * email_check +
                           ' phone' * phone_check).split()) +
                ' 입니다.'
            )

        data['permission_type_id'] = 3
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        account_id = self.user_dao.create_account(connection, data)

        data['account_id'] = account_id
        self.user_dao.create_user(connection, data)

    def sign_in_logic(self, data, connection):
        """ 유저 로그인

            Args:
                data       : View 에서 넘겨받은 dict 객체
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                token

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)}             : 잘못 입력된 키값
                403, {'message': 'invalid_user', 'error_message': '로그인에 실패했습니다.'} : 로그인 실패

            History:
                2020-12-29(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
        """

        user = self.user_dao.get_user_infomation(connection, data)
        if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
            raise InvalidUser('로그인에 실패했습니다.')

        token = self.token_generator(user)
        return token

    def token_generator(self, user):
        """ 토근 생성기

            Args:
                user : 유저

            Author: 김민구

            Returns:
                token

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)}                    : 잘못 입력된 키값
                500, {'message': 'create_token_denied', 'error_message': '로그인에 실패했습니다.'} : 토큰 생성 실패

            History:
                2020-12-29(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경
        """

        payload = {
            'account_id': user['id'],
            'username': user['username'],
            'permission_type_id': user['permission_type_id'],
            'exp': datetime.utcnow() + timedelta(hours=5)
        }

        token = jwt.encode(payload, self.config['JWT_SECRET_KEY'], self.config['JWT_ALGORITHM']).decode('utf-8')
        if not token:
            raise TokenCreateDenied('로그인에 실패했습니다.')
        return token

    def social_sign_in_logic(self, connection, data):
        """ 소셜 유저 로그인

            Args:
                data       : View 에서 넘겨받은 dict 객체
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                token

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)}                          : 잘못 입력된 키값
                403, {'message': 'invalid_user', 'error_message': '구글 소셜 로그인에 실패했습니다.'}       : 유효하지 않은 유저

            History:
                2020-12-29(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경

            Notes:
                소셜이 구글 하나라고 가정한 상황이기 때문에 확장성이 떨어짐
                확장성을 떠나서도 너무 하드코딩적인 방식
                테이블 구조를 바꿔야 합당하나 시간관계상 아래와 같이 진행
                소셜회원은 email의 아이디 뒤에 해당 "/소셜 플랫폼"을 추가
                어차피 소셜회원은 브랜디 계정 전환 전까지 일반 로그인을 할 수가 없다.(비밀번호가 없다)
                소셜회원이 브랜디 계정으로 전환할 시 "/소셜 플랫폼"을 제거해서 브랜디 회원에 해당 아이디가 존재하는 지 확인
                아이디가 없다면 그 아이디 그대로 회원가입 진행
                중복 아이디라면 아이디를 바꿔서 가입할 수 있게 만든다.
        """

        email = data['email']
        data['username'] = email.split('@')[0] + '/google'
        email_check = self.user_dao.email_exist_check(connection, data)
        if not email_check:
            data['permission_type_id'] = 3
            account_id = self.user_dao.social_create_account(connection, data)
            data['account_id'] = account_id
            self.user_dao.social_create_user(connection, data)

        user = self.user_dao.get_user_infomation(connection, data)
        if not user:
            raise InvalidUser('구글 소셜 로그인에 실패했습니다.')
        print(user)
        token = self.token_generator(user)
        return token
