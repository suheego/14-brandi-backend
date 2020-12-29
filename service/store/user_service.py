from datetime import datetime, timedelta

import bcrypt
import jwt

from utils.custom_exceptions import UserAlreadyExist, UserCreateDenied, InvalidUser


class UserService:
    """ Business Layer

        Attributes:
            user_dao: UserDao 클래스

        Author: 김민구

        History:
            2020-20-28(김민구): 초기 생성
    """

    def __init__(self, user_dao, config):
        self.user_dao = user_dao
        self.config = config

    def sign_up_service(self, data, connection):
        """ 유저생성

            Args:
                data      : View 에서 넘겨받은 dict 객체
                connection: 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                None

            Raises:
                400, {'message': 'key error', 'errorMessage': 'key_error' + format(e)}              : 잘못 입력된 키값
                403, {'message': 'user already exist', 'errorMessage': 'already_exist' + _중복 데이터} : 중복 유저 존재
                500, {'message': 'user_create_denied', 'errorMessage': 'account_create_fail'}       : account 생성 실패

            History:
                2020-20-28(김민구): 초기 생성
        """

        try:
            username_check = self.user_dao.username_exist_check(connection, data)
            email_check = self.user_dao.email_exist_check(connection, data)
            phone_check = self.user_dao.phone_exist_check(connection, data)

            if username_check or email_check or phone_check:
                raise UserAlreadyExist(
                    'already_exist' +
                    '_username' * username_check +
                    '_email' * email_check +
                    '_phone' * phone_check
                )

            data['permission_type_id'] = 3
            data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            account_id = self.user_dao.create_account(connection, data)

            if not account_id:
                raise UserCreateDenied('account_create_fail')

            data['account_id'] = account_id
            self.user_dao.create_user(connection, data)

        except KeyError as e:
            raise KeyError('key_error_' + format(e))

    def sign_in_service(self, data, connection):
        """ 유저 로그인

            Args:
                data      : View 에서 넘겨받은 dict 객체
                connection: 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                token

            Raises:
                400, {'message': 'key_error', 'errorMessage': 'key_error' + format(e)}              : 잘못 입력된 키값
                403, {'message': 'invalid_user', 'errorMessage': 'invalid_user'}                    : 로그인 실패

            History:
                2020-20-29(김민구): 초기 생성
        """

        try:
            user = self.user_dao.get_username_password(connection, data)

            if not user or bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
                raise InvalidUser('invalid_user')

            token = self.token_generator(user['account_id'], user['username'])
            return token

        except KeyError as e:
            raise KeyError('key_error_' + format(e))

    def token_generator(self, account_id, username):
        """ 토근 생성기

            Args:
                username      : 유저 이름


            Author: 김민구

            Returns:
                token

            Raises:
                400, {'message': 'key error', 'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

            History:
                2020-20-29(김민구): 초기 생성
        """
        try:
            payload = {
                'account_id' : account_id,
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=5)
            }
            token = jwt.encode(payload, self.config['JWT_SECRET_KEY'], self.config['JWT_ALGORITHM']).decode('utf-8')
            return token

        except KeyError as e:
            raise KeyError('key_error_' + format(e))
