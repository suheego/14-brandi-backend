import pymysql

from utils.custom_exceptions import DestinationNotExist

class DestinationSelectDao:

    def select_destination(self, connection, data):
        self.connection = connection
        self.data = data

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
                raise DestinationNotExist('destination_doee_not_exist')
            return result

