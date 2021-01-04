from utils.custom_exceptions import (
                                        UserAlreadyExist,
                                        UserCreateDenied,
                                        TokenCreateDenied,
                                        InvalidUser
                                    )
import bcrypt, jwt

class SellerService:

    def __init__(self, seller_dao, config):
        self.seller_dao = seller_dao
        self.config = config

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

        token = self.token_generator(seller_info['id'], seller_info['username'])

        return token

    def token_generator(self, account_id, username):

        payload = {
            'account_id' : account_id,
            'username': username,
        }

        token = jwt.encode(payload,
                           self.config['SECRET_KEY'],
                           self.config['ALGORITHM']).decode('utf-8')
        if not token:
            raise TokenCreateDenied('token_create_fail')

        return token

    def seller_search_service(self, connection, data, page, page_view):

        seller_list = self.seller_dao.get_seller_search(connection, data)
        # page_size 몇개씩 보여줄건가
        page = int(page)
        page_view = int(page_view)

        limit     = page * page_view
        offset    = limit - page_view
        seller_list  = seller_list[offset:limit]

        return seller_list



