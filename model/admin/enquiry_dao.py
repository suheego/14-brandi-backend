import pymysql
from utils.custom_exceptions import EnquiryDoesNotExist, AnswerCreateFail


class EnquiryDao:
    """ Persistence Layer

        Attributes: None

        Author: 이성보

        History:
            2020-12-28(이성보): 초기 생성 및 조회 기능 작성
            2020-12-29(이성보): q&a 검색조건별 조회 작성
            2020-12-30(이성보): q&a 상세정보 및 수정페이지 기능 작성
    """

    def get_enquiries_list(self, connection, data):
        """q&a 정보 조회

            Args:
                connection: 데이터베이스 연결 객체
                data   : 비지니스 레이어에서 넘겨 받은 딕셔너리

            Author: 이성보

            Returns:
                {
                    "enquiries": [
                        {
                            "answer": "답변입니다50",
                            "answer_date": "2020-12-28 13:31:58",
                            "answer_user": "seller8",
                            "enquiry_type": "상품 문의",
                            "id": 100,
                            "is_answered": "답변",
                            "is_secret": "비공개",
                            "membership_number": 151,
                            "phone_number": "01099990151",
                            "product_name": "성보의하루1",
                            "question": "질문이 있습니다(답변감사합니다)50",
                            "registration_date": "2020-12-28 13:31:58",
                            "seller_name": "나는셀러9"
                        },
                        {
                            "answer": "답변입니다49",
                            "answer_date": "2020-12-28 13:31:58",
                            "answer_user": "seller8",
                            "enquiry_type": "상품 문의",
                            "id": 99,
                            "is_answered": "답변",
                            "is_secret": "비공개",
                            "membership_number": 150,
                            "phone_number": "01099990150",
                            "product_name": "성보의하루1",
                            "question": "질문이 있습니다(답변감사합니다)49",
                            "registration_date": "2020-12-28 13:31:58",
                            "seller_name": "나는셀러9"
                        }
                    ],
                    "total_count": 2
                }

            History:
                2020-12-28(이성보): 초기 생성 및 조회 기능 작성
                2020-12-29(이성보): q&a 검색조건별 조회 작성
                2020-12-30(이성보): 조회된 q&a 총 갯수 반환기능 작성
            Raises:
                404, {'message': 'q&a not exist', 'errorMessage': 'q&a does not exist'} : q&a 정보 조회 실패
        """

        total_count_sql = """
                    SELECT
                        COUNT(*) AS total_count
        """

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
        """

        extra_sql = """
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
                LEFT JOIN accounts AS account 
                    ON enquiry_reply.account_id = account.id
                WHERE enquiry.is_deleted = 0
        """

        # search option 1 : 답변여부 조건
        if data['is_answered'] == 'yes':
            extra_sql += ' AND enquiry_reply.id is null'
        elif data['is_answered'] == 'no':
            extra_sql += ' AND enquiry_reply.id is not null'

        # search option 2 : 검색어 조건
        if data['product_name']:
            extra_sql += ' AND product.`name` LIKE %(product_name)s'
        elif data['id']:
            extra_sql += ' AND enquiry.id = %(id)s'
        elif data['seller_name']:
            extra_sql += ' AND seller.`name` LIKE %(seller_name)s'
        elif data['membership_number']:
            extra_sql += ' AND `user`.account_id = %(membership_number)s'

        # search option 3 : 문의유형 조건
        if data['type']:
            extra_sql += ' AND enquiry_type.id = %(type)s'

        # search option 4 : 답변소요일 조건
        if data['response_date']:
            extra_sql += ' AND enquiry.created_at BETWEEN DATE_SUB(NOW(), INTERVAL %(response_date)s DAY) AND NOW()'

        # search option 5 : 등록일 조건
        if data['start_date'] and data['end_date']:
            extra_sql += """
                AND enquiry.created_at BETWEEN CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """

        sql += extra_sql
        total_count_sql += extra_sql
        sql += ' ORDER BY enquiry.id DESC LIMIT %(page)s, %(length)s;'

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            enquiries = cursor.fetchall()
            if not enquiries:
                raise EnquiryDoesNotExist('q&a does not exist')
            cursor.execute(total_count_sql, data)
            count = cursor.fetchone()
            return {'enquiries': enquiries, 'total_count': count['total_count']}

    def get_answer_detail(self, connection, data):

        sql = """
            SELECT 
                enquiry.id,
                enquiry_type.`name` AS enquiry_type,
                account.username AS username,
                customer_information.name AS name,
                customer_information.phone AS phone,
                product.`name` AS product_name,
                product_image.image_url AS product_image,
                enquiry.content AS question,
                enquiry.created_at AS registration_date,
                CASE WHEN enquiry.is_secret = 0 THEN '비공개' ELSE '공개' END AS is_secret
            FROM 
                enquiries AS enquiry
                INNER JOIN enquiry_types AS enquiry_type 
                    ON enquiry.enquiry_type_id = enquiry_type.id
                INNER JOIN `users` AS `user` 
                    ON enquiry.user_id = `user`.account_id
                LEFT JOIN customer_information AS customer_information
                    ON `user`.account_id = customer_information.account_id
                INNER JOIN products AS product 
                    ON enquiry.product_id = product.id
                INNER JOIN product_images AS product_image
                    ON product.id = product_image.product_id
                INNER JOIN sellers AS seller
                    ON product.seller_id = seller.account_id
                LEFT JOIN enquiry_replies AS enquiry_reply 
                    ON enquiry.id = enquiry_reply.enquiry_id
                LEFT JOIN accounts AS account 
                    ON enquiry_reply.account_id = account.id
                WHERE 
                    enquiry.is_deleted = 0
                    AND enquiry.id = %(enquiry_id)s;                    
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            answer = cursor.fetchone()
            if not answer:
                raise EnquiryDoesNotExist('answer does not exist')
            return answer

    def post_answer(self, connection, data):

        validate_sql = """
        SELECT 
            EXISTS(
                SELECT id 
                FROM enquiry_replies 
                WHERE enquiry_id = %(enquiry_id)s
                AND is_deleted = 0
            ) AS validate
        """

        sql = """
            INSERT INTO
                enquiry_replies (
                content
                , enquiry_id
                , account_id
                )
            VALUES (
                %(answer)s
                , %(enquiry_id)s
                , 1
                )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(validate_sql, data)
            validate = cursor.fetchone()
            if validate['validate']:
                raise AnswerCreateFail("answer already exists")
            cursor.execute(sql, data)
            result = cursor.lastrowid
            print(result)
            if not result:
                raise AnswerCreateFail('unable_to_create')
            return result

    def put_answer(self, connection, data):

        validate_sql = """
                SELECT 
                    EXISTS(
                        SELECT id 
                        FROM enquiry_replies 
                        WHERE enquiry_id = %(enquiry_id)s
                        AND is_deleted = 0
                    ) AS validate
                """

        sql = """
                    UPDATE
                        enquiry_replies
                    SET
                        content = %(answer)s
                    WHERE
                        enquiry_id = %(enquiry_id)s
                """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(validate_sql, data)
            validate = cursor.fetchone()
            if not validate['validate']:
                raise AnswerCreateFail("answer does not exist")
            result = cursor.execute(sql, data)
            return result

    def delete_answer(self, connection, data):

        validate_sql = """
                SELECT 
                    EXISTS(
                        SELECT id 
                        FROM enquiry_replies 
                        WHERE enquiry_id = %(enquiry_id)s
                        AND is_deleted = 0
                    ) AS validate
                """

        sql = """
                    UPDATE
                        enquiry_replies
                    SET
                        is_deleted = 1
                    WHERE
                        enquiry_id = %(enquiry_id)s
                """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(validate_sql, data)
            validate = cursor.fetchone()
            if not validate['validate']:
                raise AnswerCreateFail("answer does not exist")
            result = cursor.execute(sql, data)
            return result
