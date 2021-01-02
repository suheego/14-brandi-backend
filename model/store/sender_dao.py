import traceback
import pymysql
from utils.custom_exceptions import ServerError


class SenderDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2020-12-30(고수희): 초기 생성
    """

    def get_sender_info_dao(self, connection, data):
        """ 주문자 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            return {"name": "고수희",
                    "phone": "01012341234",
                    "email": "gosuhee@gmail.com",
                    }

        History:
            2020-12-30(고수희): 초기 생성
            2020-01-02(고수희): traceback 추가
        """
        sql = """
        SELECT
        name 
        , phone 
        , email 
        FROM customer_information
        WHERE account_id = %s
        ;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data['user_id'])
                result = cursor.fetchone()
                if not result:
                    result = {
                                "name":"",
                                "phone":"",
                                "email":""
                    }
                    return result
                return result

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')
