import pymysql
from utils.custom_exceptions import SellerNotExist, SellerUpdateDenied


class SellerInfoDao:
    def get_dao(self, connection, account_id):
        account_id = account_id
        """셀러 정보 조회
        Args:   
            connection : 데이터베이스 연결 객체
            account_id  : 해당 셀러 ID  
        """

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
        account_id = account_id
        """셀러 상세 히스토리 조회
        Args:   
            connection : 데이터베이스 연결 객체
            account_id  : 해당 셀러 ID  
        """

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

    def patch_dao(self, connection, account_id):
        account_id = account_id
        """셀러 상세 히스토리 조회
        Args:   
            connection : 데이터베이스 연결 객체
            account_id  : 해당 셀러 ID  
        """
        sql = """
        UPDATE 
            seller
        SET 
            seller_discription = %(discription)s
        WHERE
            is_deleted = 0 			# 고정 값
            AND seller.account_id = %(seller_id)s;	
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(sql, account_id)
            if result == 0:
                raise SellerUpdateDenied('unable_to_update')
            return result