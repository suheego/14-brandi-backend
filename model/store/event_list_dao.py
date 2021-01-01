import traceback

import pymysql

from utils.custom_exceptions import DatabaseError


class EventListDao:
    """

    """

    def get_proceeding_event_banner_list(self, connection, page):
        """

        Args:
            connection:
            page:

        Returns:

        """

        sql = """
            SELECT 
                `event`.id AS event_id
                , `event`.banner_image
                , `event`.event_type_id
                , `event`.event_kind_id
            FROM 
                `events` AS `event`
            WHERE 
                `event`.is_display = 1
                AND `event`.is_deleted = 0
                AND now() < `event`.end_date
            ORDER BY 
                `event`.id ASC  
            LIMIT %(offset)s, %(limit)s; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, page)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_closed_event_banner_list(self, connection, data):
        """

        Args:
            connection:
            data:

        Returns:

        """

        sql = """
            SELECT 
                `event`.id AS event_id
                , `event`.banner_image
                , `event`.event_type_id
                , `event`.event_kind_id
            FROM 
                `events` AS `event`
            WHERE 
                `event`.is_display = 1
                AND `event`.is_deleted = 0
                AND now() > `event`.end_date
            ORDER BY 
                `event`.id ASC  
            LIMIT %(offset)s, %(limit)s; 
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event_information(self, connection, event_id):
        """

        Args:
            connection:
            event_id:

        Returns:

        """

        sql = """
            SELECT
                `event`.id AS event_id
                , `event`.detail_image
                , `event`.event_type_id
                , event_type.`name` AS event_type_name
                , `event`.event_kind_id
                , event_kind.`name` AS event_kind_name
                , (
                    CASE `event`.event_kind_id
                        WHEN 2 THEN 1
                        ELSE 0
                    END
                ) AS is_button
            FROM 
                `events` AS `event`
                INNER JOIN event_types AS event_type
                    ON event_type.id = `event`.event_type_id
                INNER JOIN event_kinds AS event_kind
                    ON event_kind.id = `event`.event_kind_id
            WHERE
                `event`.id = %s
                AND `event`.is_display = 1
                AND `event`.is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, event_id)
                result = cursor.fetchone()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event_button(self, connection, event_id):
        """

        Args:
            connection:
            event_id:

        Returns:

        """

        sql = """
            SELECT
                id
                , `name`
                , order_index
                , event_id
            FROM 
                event_buttons
            WHERE
                event_id = %s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, event_id)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def is_event_has_button(self, connection, event_id):
        """

        Args:
            connection:
            event_id:

        Returns:

        """

        sql = """
            SELECT
                (
                    CASE event_kind_id
                        WHEN 2 THEN 1
                        ELSE 0
                    END
                ) AS is_button
            FROM 
                `events`
            WHERE
                id = %s
                AND is_display = 1
                AND is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, event_id)
                result = cursor.fetchone()
                return result['is_button']

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event_button_product_list(self, connection, data):
        """

        Args:
            connection:
            data:

        Returns:

        """

        sql = """
            SELECT 
                product.id AS product_id
                , product_image.image_url
                , seller.`name` AS seller_name
                , product.`name` AS product_name
                , product.origin_price
                , product.discount_rate
                , product.discounted_price
                , product_sales_volume.sales_count
                , events_product.event_button_id
            FROM
                events_products AS events_product
                INNER JOIN products AS product
                    ON product.id = events_product.product_id
                INNER JOIN product_images AS product_image
                    ON product.id = product_image.product_id AND product_image.order_index = 1
                INNER JOIN sellers AS seller
                    ON seller.account_id = product.seller_id
                INNER JOIN product_sales_volumes AS product_sales_volume
                    ON product_sales_volume.product_id = product.id
            WHERE
                events_product.event_id = %(event_id)s
                AND product.is_deleted = 0
            ORDER BY
                product.id DESC
            LIMIT %(offset)s, %(limit)s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event_product_list(self, connection, data):
        """

        Args:
            connection:
            data:

        Returns:

        """

        sql = """
            SELECT 
                product.id AS product_id
                , product_image.image_url
                , seller.`name` AS seller_name
                , product.`name` AS product_name
                , product.origin_price
                , product.discount_rate
                , product.discounted_price
                , product_sales_volume.sales_count
            FROM
                events_products AS events_product
                INNER JOIN products AS product
                    ON product.id = events_product.product_id
                INNER JOIN product_images AS product_image
                    ON product.id = product_image.product_id AND product_image.order_index = 1
                INNER JOIN sellers AS seller
                    ON seller.account_id = product.seller_id
                INNER JOIN product_sales_volumes AS product_sales_volume
                    ON product_sales_volume.product_id = product.id
            WHERE
                events_product.event_id = %(event_id)s
                AND product.is_deleted = 0
                AND product.is_display = 1
            ORDER BY
                product.id DESC
            LIMIT %(offset)s, %(limit)s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')
