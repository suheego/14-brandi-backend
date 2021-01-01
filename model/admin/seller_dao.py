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


class SellerInfoDao:

    def get_seller_info(self, connection, account_id):
        """셀러 정보 조회
        Args:
            connection : 데이터베이스 연결 객체
            account_id : 해당 셀러 ID
        """
        account_id = account_id
        sql = """
        SELECT
            seller.`account_id` AS 'account_id'
            ,seller.`profile_image_url` AS 'profile_image_url'
            ,seller.`seller_status_type_id` AS 'seller_status_type_id'
            ,seller.`seller_attribute_type_id` AS 'seller_attribute_type_id'
            ,seller.`name` AS 'seller_name'
            ,seller.`english_name` AS 'seller_english_name'
            ,`account`.username AS 'username'
            ,seller.`background_image_url` AS 'background_image_url'
            ,seller.`seller_title` AS 'seller_title'
            ,seller.`seller_discription` AS 'seller_discription'
            ,seller.`contact_phone` AS 'contact_phone'
            ,seller.`contact_name` AS 'contact_name'
            ,seller.`contact_email` AS 'contact_email'


        FROM
            sellers AS seller
            INNER JOIN accounts AS `account`
                ON seller.account_id = `account`.id

        WHERE
            seller.is_deleted = 0	 	# 고정 값
            AND seller.account_id = %s;	# 변수 (화면 입력 값)
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, account_id)
            result = cursor.fetchall()
            if not result:
                raise SellerNotExist('seller_does_not_exist')
            return result

    def get_history_dao(self, connection, account_id):
        """셀러 상세 히스토리 조회
        Args:
            connection : 데이터베이스 연결 객체
            account_id  : 해당 셀러 ID
        """
        account_id = account_id
        sql = """
        SELECT
          `history`.id AS 'id'
          ,`history`.created_at AS 'updated_at'
          ,`status_type`.name AS 'seller_status'
          ,`account`.username AS 'updater_name'
        FROM
            seller_histories AS `history`
            INNER JOIN accounts AS `account`
                ON `history`.seller_id = `account`.id
            INNER JOIN seller_status_types AS `status_type`
                ON `history`.seller_status_type_id = `status_type`.id
        WHERE
            `history`.id = %s;	# 변수 (화면 입력 값)
#        ORDER BY
#            `history`.id DESC;
                """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, account_id)
            result = cursor.fetchall()
            if not result:
                raise SellerNotExist('seller_does_not_exist')
            return result

    def patch_seller_info(self, connection, data):
        """셀러 상세 히스토리 변경
        Args:   
            connection : 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 dict 객체
        """
        sql = """
        UPDATE sellers
        SET seller_title = %(seller_title)s,
            seller_discription = %(seller_discription)s
        WHERE
            is_deleted = 0 			# 고정 값
            AND sellers.account_id = %(account_id)s;	
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, data)
            if result == 0: ## 에러처리 확인예정
                raise SellerUpdateDenied('unable_to_update')
            return result

