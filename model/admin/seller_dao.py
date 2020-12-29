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

        account_sql = """
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
            cursor.execute(account_sql, data)
            account_id = cursor.lastrowid
            if not account_id:
                raise UserCreateDenied('unable_to_create_account_id')

        #data account_id 추가
        data["account_id"] = account_id
        print("첫번째")
        print(data)
        seller_sql = """
        INSERT INTO sellers 
        (   
            account_id,
            seller_attribute_type_id,
            name,
            english_name,
            contact_phone,
            service_center_number
        ) 
        VALUES (
            %(account_id)s,								
            %(seller_attribute_type_id)s,							
            %(name)s,			
            %(english_name)s,
            %(contact_phone)s,
            %(service_center_number)s			
        );
        """

        with connection.cursor() as cursor:
            cursor.execute(seller_sql, data)
            seller_id = cursor.lastrowid
            if not seller_id:
                raise UserCreateDenied('unable_to_create_seller_id')

        # data seller_id 추가
        data["seller_id"] = seller_id
        print("두번째")
        print(data)
        seller_history_sql = """
        INSERT INTO sellers_histories
        (
            seller_id,
            seller_status_type_id
        )
        VALUES (
            %(seller_id)s,
            1
        );
        """

        with connection.cursor() as cursor:
            cursor.execute(seller_history_sql, data)
            seller_id = cursor.lastrowid
            if not seller_id:
                raise UserCreateDenied('unable_to_create_seller_id')
            return seller_id