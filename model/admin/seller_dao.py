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
            ,seller.`contact_phone` AS 'contact_phone'
            ,seller.`contact_name` AS 'contact_name'
            ,seller.`contact_email` AS 'contact_email'
            ,seller.`service_center_number` AS 'service_center_number'


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

    def get_seller_search(self, connection, data):

        sql = """
        SELECT
            account.id AS account_id,
            account.username AS username,
            seller.english_name AS seller_english_name,
            seller.name AS seller_name,
            seller.contact_name AS contact_name,
            seller.contact_phone AS contact_phone,
            seller.contact_email AS contact_email,
            seller_attribute_type.name AS seller_attribute_type,
            seller_status_type.name AS seller_status_type,
            seller.updated_at AS updated_at
        
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

        if data['account_id']:
            sql += 'AND account.id = %(account_id)s '
        if data['username']:
            sql += 'AND account.username = %(username)s	'
        if data['seller_english_name']:
            sql += 'AND seller.english_name = %(seller_english_name)s'
        if data['seller_name']:
            sql += 'AND seller.name = %(seller_name)s'
        if data['contact_name']:
            sql += 'AND seller.contact_name = %(contact_name)s'
        if data['seller_status_type_name']:
            sql += 'AND seller_status_type.name = %(seller_status_type_name)s'
        if data['contact_phone']:
            sql += 'AND seller.contact_phone = %(contact_phone)s'
        if data['contact_email']:
            sql += 'AND seller.contact_email = %(contact_email)s'
        if data['seller_attribute_type_name']:
            sql += 'AND seller_attribute_type.name = %(seller_attribute_type_name)s'
        if data['start_date'] and data['end_date']:
            sql += """
                        AND seller.updated_at 
                        BETWEEN CONCAT(%(start_date)s, "00:00:00") 
                        AND CONCAT(%(end_date)s, "23:59:59")
                   """


        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql,data)
            result = cursor.fetchall()
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
            if result == 0: ## 에러처리 확인예정, 히스토리 이력은?
                raise SellerUpdateDenied('unable_to_update')
            return result

    def post_person_in_charge(self, connection, data):
        """셀러 담당자 등록
        Args:
            connection : 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 dict 객체
        """
        sql = """
        INSERT INTO additional_contacts (
            `id`
            ,`name`
            ,`phone`
            ,`email`
            ,`order_index`
            ,`seller_id`
         )
        VALUES (
            %(id)s							    # ADDITIONAL_CONTACTS ID MAX + 1 값
            ,%(name)s						    # 변수 (화면 입력 값)
            ,%(phone)s					        # 변수 (화면 입력 값)
            ,%(email)s			                # 변수 (화면 입력 값)
            ,%(order_index)s					# 변수 (화면 입력 값)
            ,%(seller_id)s						# 변수 (화면 입력 값)
        )
        ON DUPLICATE KEY UPDATE 
            `name` = %(name)s				            # 변수 (화면 입력 값)
            ,`phone` = %(phone)s			                # 변수 (화면 입력 값)
            ,`email` = %(email)s		                    # 변수 (화면 입력 값)
            ,`seller_id` = %(seller_id)s;                 # 변수 (화면 입력 값)
        
        """#순서가 1이면 패치셀러로, 그외에는 여기로 하면 되는거 아닌가??
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, data)
            if result == 0:
                raise PersonInChargeNotExist('person_in_charge_not_exist')
            return result
