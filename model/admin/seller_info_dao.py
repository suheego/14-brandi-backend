import pymysql

from utils.custom_exceptions import (
    SellerNotExist,
    SellerUpdateDenied
)

class SellerInfoDao:
    """ Persistence Layer

        Attributes: None

        Author: 이영주

        History:
            2020-12-28(이영주): 초기 생성
    """
    def get_seller_info(self, connection, account_id):
        """ 셀러 정보 조회

            Args:
                connection       : 데이터베이스 연결 객체
                account_id       : 서비스에서 넘겨 받은 객체

            Returns:
                result get_seller_info

            Raises:
                500, {'message': 'database_error', 'errorMessage': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-28(이영주): 초기 생성
        """
        account_id = account_id
        sql = """
        SELECT
            seller.`account_id` AS 'account_id',
            seller.`profile_image_url` AS 'profile_image_url',
            seller.`seller_status_type_id` AS 'seller_status_type_id',
            seller.`seller_attribute_type_id` AS 'seller_attribute_type_id',
            seller.`name` AS 'seller_name',
            seller.`english_name` AS 'seller_english_name',
            seller.`background_image_url` AS 'background_image_url',
            seller.`seller_title` AS 'seller_title',
            seller.`seller_discription` AS 'seller_discription',
            seller.`service_center_number` AS 'service_center_number'
            `account`.username AS 'username',
        FROM
            sellers AS seller
            INNER JOIN accounts AS `account`
                ON seller.account_id = `account`.id
        WHERE
            seller.is_deleted = 0	 	# 고정 값
            AND seller.account_id = %s;	# 변수 (화면 입력 값)
        """
        # ,seller.`contact_phone` AS 'contact_phone'
        # ,seller.`contact_name` AS 'contact_name'
        # ,seller.`contact_email` AS 'contact_email'
        # INNER JOIN additional_contacts AS `additional_contact`
        #     ON seller.account_id = `additional_contact`.seller_id

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, account_id)
            result = cursor.fetchall()
            if not result:
                raise SellerNotExist('seller_does_not_exist')
            return result

    def Patch_seller_info(self, connection, data):
        """셀러 정보 수정
        Args:
            connection : 데이터베이스 연결 객체
            data : service 에서 넘겨받은 객체
        """
        sql = """
        UPDATE sellers
        SET profile_image_url = %(profile_image_url)s,
            background_image_url = %(background_image_url)s,   
            shipping_information = %(shipping_information)s,
            exchange_information = %(exchange_information)s,
            seller_title = %(seller_title)s,
            seller_discription = %(seller_discription)s,
            contact_name = %(contact_name)s,
            contact_phone = %(contact_phone)s,
            contact_email = %(contact_email)s,
            post_number = %(post_number)s,
            service_center_number = %(service_center_number)s,
            address1 = %(address1)s,
            address2 = %(address2)s,
            operation_start_time = %(operation_start_time)s,
            operation_end_time = %(operation_end_time)s,
            is_weekend = %(is_weekend)s,
            weekend_operation_start_time = %(weekend_operation_start_time)s,
            weekend_operation_end_time = %(weekend_operation_end_time)s
        WHERE
            is_deleted = 0 			# 고정 값
            AND sellers.account_id = %(account_id)s;	
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, data)
            if result == 0:
                raise SellerUpdateDenied('unable_to_update')
            return result

    def patch_master_info(self, connection, data):
        """셀러 정보 수정- 마스터
        Args:
            connection : 데이터베이스 연결 객체
            data : service 에서 넘겨받은 객체
        """
        sql = """
        UPDATE sellers
        SET
            name = %(name)s,
            english_name = %(english_name)s
        WHERE
            is_deleted = 0 			# 고정 값
            AND sellers.account_id = %(account_id)s;	
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, data)
            if result == 0:
                raise SellerUpdateDenied('unable_to_update')
            return result

    def get_add_contact_info(self, connection, account_id):
        """ 추가 담당자 정보 조회

            Args:
                connection       : 데이터베이스 연결 객체
                account_id       : 서비스에서 넘겨 받은 객체

            Returns:
                result get_add_contact_info

            Raises:
                500, {'message': 'database_error', 'errorMessage': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2021-01-03(이영주): 초기 생성
        """
        account_id = account_id
        sql = """
        SELECT
            `id` AS 'id',
            `name` AS 'additional_contact_name',
            `phone` AS 'additional_contact_phone',
            `email` AS 'additional_contact_email',
            `seller_id` AS 'seller_id',
            `order_index` AS 'order_index'
        FROM
            additional_contacts
        WHERE
            is_deleted = 0 			# 고정 값
            AND sellers.account_id = %(account_id)s;	
        """
        # ORDER BY
        #     order_index ASC;
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, account_id)
            result = cursor.fetchall()
            if not result:
                raise SellerNotExist('seller_does_not_exist')
            return result

    def Patch_add_contact_info(self, connection, add_contact):
        """ 추가 담당자 정보 수정
        Args:
            connection : 데이터베이스 연결 객체
            account_id : 해당 셀러 ID
        """
        sql = """
        INSERT INTO additional_contacts (
            ,`id`
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
            `name`   = %(name)s				            # 변수 (화면 입력 값)
            ,`phone` = %(phone)s			                # 변수 (화면 입력 값)
            ,`email` = %(email)s		                    # 변수 (화면 입력 값)
            ,`seller_id` = %(seller_id)s;                 # 변수 (화면 입력 값)
         """
        print(add_contact)

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, add_contact)
            if result == 0:
                raise SellerUpdateDenied('unable_to_update')
            return result

    def Patch_seller_status(self, connection, data):
        """셀러 상태 수정
        Args:
            connection : 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 dict 객체
        """
        sql = """
            UPDATE 
                sellers
            SET 
                seller_status_type_id = %(seller_status_type_id)s
            WHERE
                is_deleted = 0 			# 고정 값
                AND sellers.account_id = %(account_id)s;	
            """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, data)
            if result == 0:
                raise SellerNotExist('unable_to_update')
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
                history.id AS id,
                history.created_at AS updated_at,
                status_type.name AS seller_status,
                account.username AS 'updater_name
            FROM
                seller_histories AS history
                INNER JOIN accounts AS account
                    ON `history`.seller_id = `account`.id
                INNER JOIN seller_status_types AS status_type
                    ON `history`.seller_status_type_id = `status_type`.id
            WHERE
                account.id = %s;
        """
        #        ORDER BY
        #            `history`.id DESC;
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, account_id)
            result = cursor.fetchall()
            if not result:
                raise SellerNotExist('seller_does_not_exist')
            return result

    def create_seller_history(self, connection, data):
        """셀러 상세 히스토리 추가
        Args:
            connection : 데이터베이스 연결 객체
            data      : service 에서 넘겨받은 dict 객체
        """
        sql = """
            INSERT INTO seller_histories (
                seller_id,
                seller_status_type_id,
                updater_id
            ) 
            VALUES (
                %(seller_id)s,
                %(seller_status_type_id)s,
                %(updater_id)s);
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, data)
            if result == 0:
                raise SellerUpdateDenied('unable_to_update')
            return result

    def patch_seller_password(self, connection, data):
        """ 셀러 패스워드 변경
            Args:
                connection : 데이터베이스 연결 객체
                data      : service 에서 넘겨받은 dict 객체
        """
        sql = """
            UPDATE 
                accounts
            SET 
                password = %(password)s
            WHERE
                is_deleted = 0 			# 고정 값
                AND accounts.id = %(account_id)s;	
            """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, data)
            if result == 0:
                raise SellerNotExist('unable_to_update')
            return result