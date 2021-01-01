import pymysql, traceback
from utils.custom_exceptions import SellerNotExist


class SellerShopDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2021-01-01(고수희): 초기 생성
    """

    def get_seller_info_dao(self, connection, data):
        """셀러 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            {
            "background_image": "https://img.freepik.com/free-psd/top-view-t-shirt-concept-mock-up_23-2148809114.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477",
            "english_name": "i am seller_2",
            "id": 2,
            "name": "나는셀러2",
            "profile_image": "https://img.freepik.com/free-psd/logo-mockup-white-paper_1816-82.jpg?size=626&ext=jpg&ga=GA1.2.1060993109.1605750477"
            }

        History:
            2021-01-01(고수희): 초기 생성

        Raises:
            400, {'message': 'seller does not exist',
            'errorMessage': 'seller_does_not_exist'} : 셀러 정보 조회 실패
        """
        sql = """
        SELECT 
        account_id AS id
        , name
        , english_name
        , profile_image_url AS profile_image
        , background_image_url AS background_image
        FROM sellers
        WHERE account_id = %s
        AND is_deleted = 0
        ; 
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data['account_id'])
            result = cursor.fetchone()
            if not result:
                raise SellerNotExist('seller_not_exist')
            return result
