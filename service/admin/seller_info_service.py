

class SellerInfoService:
    """ Business Layer

        Attributes:
            seller_info_dao : sellerinfoDao 클래스

        Author: 이영주

        History:
            2020-12-28(이영주): 초기 생성
    """

    def __init__(self, seller_dao):
        self.seller_dao = seller_dao

    def get_seller_info(self, connection, data):
        """ 셀러 상세정보 조회
            Args:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 dict 객체

            Author:
                이영주

            Raises:
                400, {'message': 'key_error', 'errorMessage': format(e)}                            : 잘못 입력된 키값

            History:
                2020-12-28(이영주): 초기 생성
        """
        try:
            account_id = data['account_id']
            result_seller_info = self.seller_dao.get_seller_info(connection, account_id)
            return result_seller_info

        except KeyError:
            raise KeyError('Key_error')

    def get_add_contact_info(self, connection, data):
        """ 추가 담당자정보 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 dict 객체

            Author:
                이영주

            Raises:
                400, {'message': 'key_error', 'errorMessage': format(e)}                            : 잘못 입력된 키값

            History:
                2021-01-03(이영주): 초기 생성
        """
        try:
            account_id = data['account_id']
            result_get_add_contact_info = self.seller_dao.get_add_contact_info(connection, account_id)
            return result_get_add_contact_info

        except KeyError:
            raise KeyError('Key_error')

    def patch_seller_info(self, connection, data):
        """ 셀러 정보 수정

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author:
            이영주

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2020-12-30(이영주): 초기 생성
        """
        try:
            return self.seller_dao.Patch_seller_info(connection, data)

        except KeyError:
            raise KeyError('Key_error')

    def patch_master_info(self, connection, data):
        """ 셀러 정보 수정

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author:
            이영주

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2020-12-30(이영주): 초기 생성
        """
        try:
            if data['permission_types'] == "1":
                self.seller_dao.patch_master_info(connection, data)

        except KeyError:
            raise KeyError('Key_error')

    def patch_add_contact(self, connection, data):
        """ 추가 담당자 수정

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author:
            이영주

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2020-12-30(이영주): 초기 생성
        """
        try:
            if data['add_contact'] != 1:
                add_contact = {
                          'id': data['add_contact']['id'],
                          'name': data['add_contact']['name'],
                          'phone': data['add_contact']['phone'],
                          'email': data['add_contact']['email'],
                          'order_index': data['add_contact']['order_index'],
                          'seller_id': data['add_contact']['seller_id']
                }
            return self.seller_dao.Patch_add_contact_info(connection, add_contact)

        except KeyError:
            raise KeyError('Key_error')

    def patch_seller_status(self, connection, data):
        """ 셀러 정보 수정

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 이영주

        Returns:
            return

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2021-01-03(이영주): 초기 생성
        """
        try:
            self.seller_dao.Patch_seller_status(connection, data)

        except KeyError:
            raise KeyError('Key_error')

    def get_seller_history(self, connection, data):
        """ 해당 아이디를 가진 셀러 히스토리 검색 함수

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author:
            이영주

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

    def patch_seller_history(self, connection, data):
        """ 해당 아이디를 가진 셀러 정보 업데이트

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author:
            이영주

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2020-12-29(이영주): 초기 생성/ 작업중
        """

        try:
            self.seller_dao.create_seller_history(connection, data)

        except KeyError:
            raise KeyError('Key_error')

    def patch_seller_password(self, connection, data):
        """ 셀러 패스워드 변경

            Args:
                connection: 데이터베이스 연결 객체
                account_id      : View 에서 넘겨받은 객체

            Author:
                이영주

            Raises:
                400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

            History:
                2021-01-04(이영주): 초기 생성
        """

        try:

            self.seller_dao.patch_seller_password(connection, data)

        except KeyError:
            raise KeyError('Key_error')