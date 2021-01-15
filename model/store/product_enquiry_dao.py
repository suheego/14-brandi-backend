import pymysql

from utils.custom_exceptions import DatabaseError


class ProductEnquiryDao:
    """ Persistence Layer

        Attributes: None

        Author: 김민구

        History:
            2020-01-04 초기 생성
    """

    def get_enquiry_type_list(self, connection):
        """ 질문 유형 리스트를 조회

        Args:
            connection: 데이터베이스 연결 객체

        Returns: 질문 유형이 담긴 리스트 반환
            [
                {
                    "id": 1,
                    "name": "상품 문의"
                }
            ]

        Raises:
            500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

        History:
                2021-01-04(김민구): 초기 생성
        """

        sql = """
            SELECT
                id,
                name
            FROM
                enquiry_types
            WHERE
                is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_product_enquiry_list(self, connection, data):
        """ 상품 질문 리스트를 조회

        Args:
            connection: 데이터베이스 연결 객체
            data: 서비스에서 넘겨 받은 dict (type, offset, limit)
                type = self 혹은 all
                offset = 0부터 시작(5단위)

        Returns: 질문이 담긴 리스트 반환
            [
                {
                    "content": "임시질문인데요2(답변감사합니다)",
                    "created_at": "2021-01-04 11:31:26",
                    "enquiry_id": 102,
                    "enquiry_type_id": 1,
                    "enquiry_type_name": "상품 문의",
                    "is_completed": 1,
                    "is_secret": 0,
                    "product_id": 1,
                    "user_id": 152
                }
            ]

        Raises:
            500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

        History:
                2021-01-04(김민구): 초기 생성
        """

        sql = """
            SELECT 
                enquiry.id 
                , enquiry.product_id
                , enquiry.user_id
                , enquiry.content
                , enquiry.enquiry_type_id
                , enquiry_type.`name` AS enquiry_type_name
                , enquiry.is_secret
                , enquiry.is_completed
                , enquiry.created_at
            FROM
                enquiries AS enquiry
                INNER JOIN enquiry_types AS enquiry_type
                    ON enquiry_type.id = enquiry.enquiry_type_id
            WHERE 
                enquiry.product_id = %(product_id)s
                AND enquiry.is_deleted = 0
        """

        try:
            if 'user_id' in data:
                sql += '''
                AND enquiry.user_id = %(user_id)s
                '''

            sql += '''
            ORDER BY 
                enquiry.id DESC
            LIMIT %(offset)s, %(limit)s
            '''

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_enquiry_reply_list(self, connection, data):
        """ 답변 리스트를 조회

        Args:
            connection: 데이터베이스 연결 객체
            data: 서비스에서 넘겨 받은 dict
                enquiry_ids = 질문 아이디들이 담긴 튜플

        Returns: 답변이 담긴 리스트 반환
            [
                {
                    "account_id": 2,
                    "content": "답변드릴게요",
                    "created_at": "2021-01-04 12:38:12",
                    "enquiry_id": 102,
                    "id": 52,
                    "seller_name": "나는셀러2"
                }
            ]

        Raises:
            500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러
            400, {'message': 'key_error', 'error_message': format(e)}                           : 잘못 입력된 키값

        History:
                2021-01-04(김민구): 초기 생성
        """

        sql = """
            SELECT
                enquiry_reply.id
                , enquiry_reply.content
                , enquiry_reply.account_id
                , seller.`name` AS seller_name
                , enquiry_reply.created_at
                , enquiry_reply.enquiry_id
            FROM
                enquiry_replies AS enquiry_reply
                INNER JOIN sellers AS seller
                    ON seller.account_id = enquiry_reply.account_id
            WHERE
                enquiry_reply.is_deleted = 0
                AND enquiry_reply.enquiry_id IN %(enquiry_ids)s

        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = {row['enquiry_id']: row for row in cursor.fetchall()}
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_my_page_enquiry_list(self, connection, data):
        """ my-page 질문 리스트를 조회

        Args:
            connection: 데이터베이스 연결 객체
            data: 서비스에서 넘겨 받은 dict (type, offset, limit, user_id)
                type = wait, complete, all
                offset = 0부터 시작(5단위)

        Returns: my-page 질문이 담긴 리스트 반환
            [
                {
                    "content": "임시질문인데요2(답변감사합니다)",
                    "created_at": "2021-01-04 11:31:26",
                    "enquiry_id": 102,
                    "enquiry_type_id": 1,
                    "enquiry_type_name": "상품 문의",
                    "is_completed": 1,
                    "is_secret": 0,
                    "product_id": 1,
                    "user_id": 152
                }
            ]

        Raises:
            500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러
            400, {'message': 'key_error', 'error_message': format(e)}                           : 잘못 입력된 키값

        History:
                2021-01-04(김민구): 초기 생성
        """

        sql = """
            SELECT 
                enquiry.id 
                , enquiry.product_id
                , enquiry.user_id
                , enquiry.content
                , enquiry.enquiry_type_id
                , enquiry_type.`name` AS enquiry_type_name
                , enquiry.is_secret
                , enquiry.is_completed
                , enquiry.created_at
            FROM
                enquiries AS enquiry
                INNER JOIN enquiry_types AS enquiry_type
                    ON enquiry_type.id = enquiry.enquiry_type_id
            WHERE 
                enquiry.is_deleted = 0
                AND enquiry.user_id = %(user_id)s
        """

        try:
            if data['type'] == 'complete':
                sql += """
                AND enquiry.is_completed = 1
                """
            elif data['type'] == 'wait':
                sql += """
                AND enquiry.is_completed = 0
                """

            sql += """
            ORDER BY 
                enquiry.id DESC
            LIMIT %(offset)s, %(limit)s
            """

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception:
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')