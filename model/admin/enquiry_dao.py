import pymysql
from utils.custom_exceptions import UserNotExist


class EnquiryDao:

    def get_dao(self, connection, data):

        total_count_sql = """
                    SELECT
                        COUNT(*) AS total_count
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
        """

        total_count_sql += ' WHERE enquiry.is_deleted = 0'
        sql += ' WHERE enquiry.is_deleted = 0'

        if data['is_answered'] == 'yes':
            total_count_sql += ' AND EXISTS (SELECT id FROM enquiries WHERE enquiries.id = enquiry_reply.enquiry_id)'
            sql += ' AND EXISTS (SELECT id FROM enquiries WHERE enquiries.id = enquiry_reply.enquiry_id)'
        elif data['is_answered'] == 'no':
            total_count_sql += ' AND NOT EXISTS (SELECT id FROM enquiries WHERE enquiries.id = enquiry_reply.enquiry_id)'
            sql += ' AND NOT EXISTS (SELECT id FROM enquiries WHERE enquiries.id = enquiry_reply.enquiry_id)'

        if data['product_name']:
            total_count_sql += ' AND product.`name` LIKE %(product_name)s'
            sql += ' AND product.`name` LIKE %(product_name)s'
        elif data['id']:
            total_count_sql += ' AND enquiry.id = %(id)s'
            sql += ' AND enquiry.id = %(id)s'
        elif data['seller_name']:
            total_count_sql += ' AND seller.`name` LIKE %(seller_name)s'
            sql += ' AND seller.`name` LIKE %(seller_name)s'
        elif data['membership_number']:
            total_count_sql += ' AND `user`.account_id = %(membership_number)s'
            sql += ' AND `user`.account_id = %(membership_number)s'

        if data['type'] == 'product_enquiry':
            total_count_sql += ' AND enquiry_type.id = 1'
            sql += ' AND enquiry_type.id = 1'
        elif data['type'] == 'exchange':
            total_count_sql += ' AND enquiry_type.id = 2'
            sql += ' AND enquiry_type.id = 2'
        elif data['type'] == 'faulty':
            total_count_sql += ' AND enquiry_type.id = 3'
            sql += ' AND enquiry_type.id = 3'
        elif data['type'] == 'other':
            total_count_sql += ' AND enquiry_type.id = 4'
            sql += ' AND enquiry_type.id = 4'
        elif data['type'] == 'shipping_enquiry':
            total_count_sql += ' AND enquiry_type.id = 5'
            sql += ' AND enquiry_type.id = 5'
        elif data['type'] == 'one_day_delivery':
            total_count_sql += ' AND enquiry_type.id = 6'
            sql += ' AND enquiry_type.id = 6'
        elif data['type'] == 'cancel_change':
            total_count_sql += ' AND enquiry_type.id = 7'
            sql += ' AND enquiry_type.id = 7'

        if data['response_date'] == 1:
            sql += ' AND enquiry.created_at BETWEEN DATE_SUB(NOW(), INTERVAL 1 DAY) AND NOW()'
        elif data['response_date'] == 3:
            sql += ' AND enquiry.created_at BETWEEN DATE_SUB(NOW(), INTERVAL 3 DAY) AND NOW()'
        elif data['response_date'] == 7:
            sql += ' AND enquiry.created_at BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW()'
        elif data['response_date'] == 15:
            sql += ' AND enquiry.created_at BETWEEN DATE_SUB(NOW(), INTERVAL 15 DAY) AND NOW()'
        elif data['response_date'] == 30:
            sql += ' AND enquiry.created_at BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()'

        if data['start_date'] and data['end_date']:
            total_count_sql += """
                           AND enquiry.created_at BETWEEN CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """
            sql += """
                AND enquiry.created_at BETWEEN CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """

        sql += ' ORDER BY enquiry.id DESC LIMIT %(page)s, %(length)s;'
        print(sql)

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            enquiries = cursor.fetchall()
            if not enquiries:
                raise UserNotExist('user_does_not_exist')
            cursor.execute(total_count_sql, data)
            count = cursor.fetchone()
            return {'enquiries': enquiries, 'total_count': count['total_count']}

# total_count_sql sql 통합
# if not enquiries 위치
