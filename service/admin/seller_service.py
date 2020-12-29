

class SellerInfoService:

    def __init__(self, seller_dao):
        self.seller_dao = seller_dao

    def get_seller_info_service(self, connection, data):
        """해당 아이디를 가진 셀러 상세정보 검색 함수

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 이영주

        Returns:
                "result": [
        {
            "account_id": 50,
            "background_image_url": "https://img.freepik.com/free-psd/top-view-t-shirt-concept-mock-up_23-2148809114.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477",
            "profile_image_url": "https://img.freepik.com/free-psd/logo-mockup-white-paper_1816-82.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477",
            "seller_attribute_type_id": 2,
            "seller_english_name": "i am seller_50",
            "seller_name": "나는셀러50",
            "seller_status_type_id": 3,
            "username": "seller49"
        }
    ]

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2020-12-28(이영주): 초기 생성/ 작업중
        """
        try:
            account_id = data['account_id']
            return self.seller_dao.get_dao(connection, account_id)

        except KeyError:
            raise KeyError('Key_error')

    def get_seller_history_service(self, connection, data):
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

    def patch_seller_info_service(self, connection, data):
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
            account_id = data['account_id']
            return self.seller_dao.pacth_dao(connection, account_id)

        except KeyError:
            raise KeyError('Key_error')