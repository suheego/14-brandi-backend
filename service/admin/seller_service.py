from utils.custom_exceptions import (
                                        UserAlreadyExist,
                                        UserCreateDenied,
                                        TokenCreateDenied,
                                        InvalidUser
                                    )
import bcrypt, jwt

class SellerService:

    def __init__(self, seller_dao,config):
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

      
class SellerInfoService:

    def __init__(self, seller_dao):
        self.seller_dao = seller_dao

    def get_seller_info(self, connection, data):
        """해당 아이디를 가진 셀러 상세정보 검색 함수
        seller_dao 의 get_seller_info 함수로 전달
        Args:
            connection : 데이터베이스 연결 객체
            data       : seller 계정
        Author:
            이영주
        Returns:
            result_seller_info(dao로 전달)
        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값
        History:
            2020-12-28(이영주): 초기 생성
        """
        try:
            account_id = data['account_id']
            result_seller_info = self.seller_dao.get_seller_info(connection, account_id)
            return result_seller_info

        except KeyError:
            raise KeyError('Key_error')

    def get_seller_history(self, connection, data):
        """해당 아이디를 가진 셀러 히스토리 검색 함수
        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체
        Author: 이영주
        Returns:
                "result": [
                    {
                        "id": 50,
                        "seller_status": "휴점",
                        "updated_at": "Thu, 24 Dec 2020 23:31:43 GMT",
                        "updater_name": "seller50"
                    }
                ]
        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값
        History:
            2020-12-29(이영주): 초기 생성/ 작업중
        """
        try:
            account_id = data['account_id']
            return self.seller_dao.get_history_dao(connection, account_id)

        except KeyError:
            raise KeyError('Key_error')

    def patch_seller_info(self, connection, data):
        """해당 아이디를 가진 셀러 정보 업데이트
        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체
        Author: 이영주
        Returns:
            return
        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2020-12-29(이영주): 초기 생성/ 작업중
        """

        try:
            return self.seller_dao.patch_seller_info(connection, data)

        except KeyError:

            raise KeyError('Key_error')

    def post_person_in_charge(self, connection, data):
        """해당 아이디를 가진 셀러 정보 업데이트

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 이영주

        Returns:
            return

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2020-12-30(이영주): 초기 생성
        """
        try:
#            if data['order_index'] == 1:
#            return self.seller_dao.patch_seller_info(connection, data)



            return self.seller_dao.post_person_in_charge(connection, data) #추가 담당자 로직



# 그 해당 값이 동시에 들어올 수 있으니까 get 리스트를 써야하는게 맞dma
        except KeyError:
             raise KeyError('Key_error')


        # get dao를 또 만들어야하는지?

