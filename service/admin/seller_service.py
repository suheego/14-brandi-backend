from utils.custom_exceptions import (
                                        UserAlreadyExist,
                                        UserCreateDenied,
                                        TokenCreateDenied,
                                        InvalidUser
                                    )
import bcrypt, jwt
from model          import SellerDao

from flask                   import jsonify


class SellerService:

    def __init__(self, config):
        self.config = config
        self.seller_dao = SellerDao()

    def seller_signup_service(self, connection, data):

        # 중복검사
        username = self.seller_dao.get_username(connection, data)
        if username:
            print("username exist")
            raise UserAlreadyExist('already_exist')

        # password hash
        data['password'] = bcrypt.hashpw(
            data['password'].encode('UTF-8'),
            bcrypt.gensalt()
        ).decode('UTF-8')

        # permission_type : 셀러[2]
        data['permission_type_id'] = 2

        # account 생성
        account_id = self.seller_dao.create_account_dao(connection, data)
        data['account_id'] = account_id

        # seller 생성
        create_seller_result = self.seller_dao.create_seller_dao(connection, data)
        if not create_seller_result:
            raise UserCreateDenied('unable_to_create_seller')

        # seller_history 생성
        create_seller_history_result = self.seller_dao.create_seller_history_dao(connection, data)
        if not create_seller_history_result:
            raise UserCreateDenied('unable_to_create_seller_history')

    def seller_signin_service(self, connection, data):

        seller_info = self.seller_dao.get_seller_infomation(connection, data)

        if not seller_info or not bcrypt.checkpw(data['password'].encode('utf-8'),seller_info['password'].encode('utf-8')):
            raise InvalidUser('invalid_user')

        token = self.token_generator(seller_info)

        return token

    def token_generator(self, seller_info):

        payload = {
            'account_id': seller_info['id']
            ,'username' : seller_info['username']
            ,'permission_type_id' : seller_info['permission_type_id']
        }

        token = jwt.encode(payload,
                            self.config['JWT_SECRET_KEY'],
                            self.config['JWT_ALGORITHM']).decode('utf-8')
        if not token:
            raise TokenCreateDenied('token_create_fail')

        return token


    def seller_search_service(self, connection, data, page, page_view):

        data['limit'] = int(page) * int(page_view)
        data['offset'] = data['limit'] - int(page_view)
        seller_info = self.seller_dao.get_seller_search(connection, data)

        return seller_info


    def seller_list_service(self, connection, offset):
        seller_list = self.seller_dao.get_seller_list(connection, offset)
        if not seller_list:
            return []
        return seller_list


      
