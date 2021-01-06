import pymysql
from datetime                import datetime

from utils.custom_exceptions import (
    UserUpdateDenied,
    UserCreateDenied,
    UserNotExist,
    SellerNotExist,
    SellerUpdateDenied
)


class SellerDao:

    def get_username(self, connection, data):

        sql = """
            SELECT *
            FROM accounts
            WHERE username = %s;
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data['username'])
            result = cursor.fetchall()
            return result

    def create_account_dao(self, connection, data):

        sql = """
        INSERT INTO ACCOUNTS
        (
            username,
            password,
            permission_type_id
        )
        VALUES(
            %(username)s,
            %(password)s,
            2
        );
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            account_id = cursor.lastrowid

            if not account_id:
                raise UserCreateDenied('unable_to_create_account_id')
            return account_id

    def create_seller_dao(self, connection, data):
        sql = """
        INSERT INTO SELLERS
        (
            account_id
            ,seller_attribute_type_id
            ,name
            ,english_name
            ,contact_phone
            ,service_center_number
        ) VALUES (
            %(account_id)s
            ,%(seller_attribute_type_id)s
            ,%(name)s
            ,%(english_name)s
            ,%(contact_phone)s
            ,%(service_center_number)s
        );
        """
        with connection.cursor() as cursor:
            result = cursor.execute(sql, data)
            return result

    def create_seller_history_dao(self, connection, data):
        sql = """
        INSERT INTO seller_histories
        (
            seller_id
            ,seller_status_type_id
            ,updater_id
        )
        VALUES(
            %(account_id)s
            ,1
            ,%(account_id)s
        );
        """

        with connection.cursor() as cursor:
            result = cursor.execute(sql, data)
            return result


    def get_seller_infomation(self, connection, data):

        sql = """
        SELECT
            id
            , username
            , password
            , permission_type_id 
        FROM
            accounts
        WHERE
            is_deleted = 0
            AND username = %(username)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchone()
            return result



    def get_seller_search(self, connection, data):

        total_count_sql = """
            SELECT
                COUNT(*) AS total_count
        """
        product_registration_number = """
            SELECT 
                COUNT(*) AS products_count
            FROM
                seller AS seller
                
                INNER JOIN products AS product
                    ON seller.account_id = product.seller_id

            WHERE 
                seller.is_deleted = 0
                AND account.permission_type_id = 2 
        """
        sql = """
            SELECT
                account.id AS account_id
                ,account.username AS username
                ,seller.english_name AS seller_english_name
                ,seller.name AS seller_name
                ,seller.contact_name AS contact_name
                ,seller.contact_phone AS contact_phone
                ,seller.contact_email AS contact_email
                ,seller_attribute_type.name AS seller_attribute_type
                ,seller_status_type.name AS seller_status_type
                ,seller.updated_at AS updated_at
            """

        extra_sql = """
            FROM
                sellers AS seller

                INNER JOIN accounts AS `account`
                    ON seller.account_id = `account`.id
                INNER JOIN seller_status_types AS seller_status_type
                    ON seller.seller_status_type_id = seller_status_type.id
                INNER JOIN seller_attribute_types AS seller_attribute_type
                    ON seller.seller_attribute_type_id = seller_attribute_type.id

            WHERE
                seller.is_deleted = 0
                AND account.permission_type_id = 2 
            """

        filter_sql = ' ORDER BY `account`.id DESC LIMIT %(offset)s, %(limit)s'

        if data['account_id']:
            sql += ' AND account.id = %(account_id)s '
        if data['username']:
            sql += ' AND account.username = %(username)s	'
        if data['seller_english_name']:
            sql += ' AND seller.english_name = %(seller_english_name)s'
        if data['seller_name']:
            sql += ' AND seller.name = %(seller_name)s'
        if data['contact_name']:
            sql += ' AND seller.contact_name = %(contact_name)s'
        if data['seller_status_type_name']:
            sql += ' AND seller_status_type.name = %(seller_status_type_name)s'
        if data['contact_phone']:
            sql += ' AND seller.contact_phone = %(contact_phone)s'
        if data['contact_email']:
            sql += ' AND seller.contact_email = %(contact_email)s'
        if data['seller_attribute_type_name']:
            sql += ' AND seller_attribute_type.name = %(seller_attribute_type_name)s'
        if data['start_date'] and data['end_date']:
            sql += """
                        AND seller.updated_at 
                        BETWEEN CONCAT(%(start_date)s, "00:00:00") 
                        AND CONCAT(%(end_date)s, "23:59:59")
                   """

        sql += extra_sql + filter_sql
        total_count_sql += extra_sql

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            sellers = cursor.fetchall()
            if not sellers:
                raise SellerNotExist('seller does not exist')
            cursor.execute(total_count_sql, data)
            count = cursor.fetchone()

            return {'seller_list':sellers, 'total_count':count['total_count']}


    def get_seller_list(self, connection, offset):
        sql = """
            SELECT
                account.id AS account_id
                ,account.username AS username
                ,seller.english_name AS seller_english_name
                ,seller.name AS seller_name
                ,seller.contact_name AS contact_name
                ,seller.contact_phone AS contact_phone
                ,seller.contact_email AS contact_email
                ,seller_attribute_type.name AS seller_attribute_type
                ,seller_status_type.name AS seller_status_type
                ,seller.updated_at AS updated_at
            FROM
                sellers AS seller

                INNER JOIN accounts AS `account`
                    ON seller.account_id = `account`.id
                INNER JOIN seller_status_types AS seller_status_type
                    ON seller.seller_status_type_id = seller_status_type.id
                INNER JOIN seller_attribute_types AS seller_attribute_type
                    ON seller.seller_attribute_type_id = seller_attribute_type.id
            
            WHERE
                seller.is_deleted = 0
            
            ORDER BY account.id DESC 
            LIMIT 0, %s
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, offset)
            sellers = cursor.fetchall()
            if not sellers:
                raise SellerNotExist('seller does not exist')

            return sellers



