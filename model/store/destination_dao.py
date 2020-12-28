import pymysql

from utils.custom_exceptions import DestinationNotExist, DestinationCreateDenied


class DestinationSelectDao:

    def select_destination(self, connection, data):

        sql = """
            SELECT
                id
                , user_id
                , recipient
                , phone
                , address1
                , address2
                , post_number
                , default_location
            FROM
                destinations
            WHERE
                id = %(destination_id)s;
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if not result:
                raise DestinationNotExist('destination_does_not_exist')
            return result

    def create_destination_dao(self, connection, data):

        sql ="""
        INSERT INTO destinations (
            user_id
            , recipient
            , phone
            , address1
            , address2
            , post_number
            , default_location
        ) VALUES (
            %(user_id)s
            , %(recipient)s
            , %(phone)s
            , %(address1)s
            , %(address2)s
            , %(post_number)s
            , %(default_location)s
        );
        """
        with connection.cursor() as cursor:
            affected_row = cursor.execute(sql, data)
            print(affected_row)
            if affected_row == 0:
                raise DestinationCreateDenied('unable_to_create')

#    def check_account_type(self, connectoin, account_id):
#        
#        sql ="""
#        SELECT permission_type
#        FROM 
#
