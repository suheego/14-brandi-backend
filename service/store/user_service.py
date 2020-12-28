import bcrypt

from utils.custom_exceptions import UserAlreadyExist


class UserService:
    """ Business Layer

        Attributes:
            user_dao: UserDao 클래스

        Author: 김민구

        History:
            2020-20-28(김민구): 초기 생성
    """

    def __init__(self, user_dao):
        self.user_dao = user_dao

    def signup_service(self, data, connection):
        try:
            result = self.user_dao.user_exist_check(connection, data)

            if result:
                raise UserAlreadyExist('user_already')

            data['permission_type_id'] = 3
            data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            account_id = self.user_dao.create_account(connection, data)
            data['account_id'] = account_id
            self.user_dao.create_user(connection, data)

        except KeyError as e :
            raise KeyError('key error ' + format(e))
