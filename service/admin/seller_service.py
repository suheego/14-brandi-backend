from utils.custom_exceptions import UserAlreadyExist
import bcrypt
import jwt

class SellerService:

    def __init__(self, seller_dao):
        self.seller_dao = seller_dao

    def check_account_service(self, connection, data):
        try:
            # 중복검사
            username = self.seller_dao.get_username(connection, data)

            if username:
                print("username exist")
                raise UserAlreadyExist('already_exist')

            data['password'] = self.change_password_hash_service(data['password'])

            return self.seller_dao.create_account_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')

    def change_password_hash_service(self, password):
        # password hash 로 변경해주는 함수
        hashed_password = bcrypt.hashpw(
            password.encode('UTF-8'),
            bcrypt.gensalt()
        ).decode('UTF-8')
        return hashed_password


    # def post_seller_insert_service(self, connection, data):
    #    return self.seller_dao.create_seller_dao(connection, data)
    #
    # def post_seller_history_insert_service(self, connection, data):
    #     try:


