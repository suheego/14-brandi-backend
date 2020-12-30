import pymysql, datetime
from utils.custom_exceptions import UserUpdateDenied, UserCreateDenied, UserNotExist

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
            ,username
            ,password
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

