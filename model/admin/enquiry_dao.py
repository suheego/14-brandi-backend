import pymysql
from utils.custom_exceptions import EnquiryDoesNotExist


class EnquiryDao:
    """ Persistence Layer

        Attributes: None

        Author: 이성보

        History:
            2020-12-29(이성보): 초기 생성 및 조회 기능 작성
            2020-12-30(이성보): Q&A 검색조건별 조회 작성
        """

    def get_enquiries_list(self, connection, data):
        """Q&A 정보 조회

            Args:
                connection: 데이터베이스 연결 객체
                data   : 비지니스 레이어에서 넘겨 받은 검색 조건 키벨류

            Author: 이성보

            Returns:
                return [
                    {
                        "created_at": "Mon, 28 Dec 2020 16:40:41 GMT",
                        "end_date": "Mon, 01 Mar 2021 00:00:00 GMT",
                        "event_kind": "버튼",
                        "event_name": "성보의 하루 시리즈2(버튼형)",
                        "event_number": 2,
                        "event_status": "진행중",
                        "event_type": "상품(이미지)",
                        "is_display": "노출",
                        "product_count": 59,
                        "start_date": "Mon, 19 Oct 2020 00:00:00 GMT"
                    },
                    {
                        "created_at": "Mon, 28 Dec 2020 16:40:41 GMT",
                        "end_date": "Mon, 01 Mar 2021 00:00:00 GMT",
                        "event_kind": "상품",
                        "event_name": "성보의 하루 시리즈",
                        "event_number": 1,
                        "event_status": "진행중",
                        "event_type": "상품(이미지)",
                        "is_display": "노출",
                        "product_count": 40,
                        "start_date": "Mon, 19 Oct 2020 00:00:00 GMT"
                    }
                ]

            History:
                2020-12-29(이성보): 초기 생성 및 조회 기능 작성
                2020-12-30(이성보): Q&A 검색조건별 조회 작성

            Raises:
                400, {'message': 'q&a not exist', 'errorMessage': 'q&a does not exist'} : Q&A 정보 조회 실패
        """

        # COUNT(*) AS total_count
        sql = """
            SELECT 
                enquiry.id,
                enquiry_type.`name` AS enquiry_type,
                enquiry.created_at AS registration_date,
                `user`.phone AS phone_number,
                product.`name` AS product_name,
                enquiry.content AS question,
                `user`.account_id AS membership_number,
                seller.`name` AS seller_name,
                CASE WHEN enquiry.is_secret = 0 THEN '비공개' ELSE '공개' END AS is_secret,
                CASE WHEN enquiry_reply.enquiry_id = enquiry.id THEN '답변' ELSE '미답변' END AS is_answered,
                enquiry_reply.content AS answer,
                enquiry_reply.created_at AS answer_date,
                account.username AS answer_user
            FROM 
                enquiries AS enquiry
                INNER JOIN enquiry_types AS enquiry_type 
                    ON enquiry.enquiry_type_id = enquiry_type.id
                INNER JOIN `users` AS `user` 
                    ON enquiry.user_id = `user`.account_id
                INNER JOIN products AS product 
                    ON enquiry.product_id = product.id
                INNER JOIN sellers AS seller
                    ON product.seller_id = seller.account_id
                LEFT JOIN enquiry_replies AS enquiry_reply 
                    ON enquiry.id = enquiry_reply.enquiry_id
                INNER JOIN accounts AS account 
                    ON enquiry_reply.account_id = account.id
                WHERE enquiry.is_deleted = 0
        """

        # search option 1 : search by keyword (event_name or event_number)
        if data['is_answered'] == 'yes':
            sql += ' AND EXISTS (SELECT id FROM enquiries WHERE enquiries.id = enquiry_reply.enquiry_id)'
        elif data['is_answered'] == 'no':
            sql += ' AND NOT EXISTS (SELECT id FROM enquiries WHERE enquiries.id = enquiry_reply.enquiry_id)'

        # search option 1 : search by keyword (event_name or event_number)
        if data['product_name']:
            sql += ' AND product.`name` LIKE %(product_name)s'
        elif data['id']:
            sql += ' AND enquiry.id = %(id)s'
        elif data['seller_name']:
            sql += ' AND seller.`name` LIKE %(seller_name)s'
        elif data['membership_number']:
            sql += ' AND `user`.account_id = %(membership_number)s'

        # search option 1 : search by keyword (event_name or event_number)
        if data['type'] == 'product_enquiry':
            sql += ' AND enquiry_type.id = 1'
        elif data['type'] == 'exchange':
            sql += ' AND enquiry_type.id = 2'
        elif data['type'] == 'faulty':
            sql += ' AND enquiry_type.id = 3'
        elif data['type'] == 'other':
            sql += ' AND enquiry_type.id = 4'
        elif data['type'] == 'shipping_enquiry':
            sql += ' AND enquiry_type.id = 5'
        elif data['type'] == 'one_day_delivery':
            sql += ' AND enquiry_type.id = 6'
        elif data['type'] == 'cancel_change':
            sql += ' AND enquiry_type.id = 7'

        # search option 1 : search by keyword (event_name or event_number)
        if data['response_date']:
            sql += ' AND enquiry.created_at BETWEEN DATE_SUB(NOW(), INTERVAL %(response_date)s DAY) AND NOW()'

        # search option 1 : search by keyword (event_name or event_number)
        if data['start_date'] and data['end_date']:
            sql += """
                AND enquiry.created_at BETWEEN CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """

        sql += ' ORDER BY enquiry.id DESC LIMIT %(page)s, %(length)s;'

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            enquiries = cursor.fetchall()
            if not enquiries:
                raise EnquiryDoesNotExist('q&a does not exist')
            return {'enquiries': enquiries}  # 'total_count': count['total_count']

# total_count_sql sql 통합
# if not enquiries 위치
