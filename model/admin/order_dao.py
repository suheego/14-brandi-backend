import pymysql
import traceback
from utils.custom_exceptions import (OrderDoesNotExist,
                                     UnableToUpdate,
                                     DoesNotOrderDetail,
                                     DeniedUpdate,
                                     )


class OrderDao:
    """ Persistence Layer

        Attributes: None

        Author: 김민서

        History:
            2020-2012-29(김민서): 초기 생성
            2020-12-30(김민서): 1차 수정
            2020-12-31(김민서): 2차 수정
    """

    def get_order_list_dao(self, connection, data):
        total_count_sql = """
            SELECT COUNT(*) AS total_count
        """

        sql = """
            SELECT 
                order_item.id,
                order_item.created_at AS created_at_date,
                order_item.updated_at AS updated_at_date,
                `order`.order_number AS order_number,
                order_item.order_detail_number AS order_detail_number,
                seller.`name` AS seller_name,
                product.`name` AS product_name,
                CONCAT(color.`name`, '/', size.`name`) AS option_information,
                stock.extra_cost AS option_extra_cost,
                order_item.quantity AS quantity,
                `order`.sender_name AS customer_name,
                `order`.sender_phone AS customer_phone,
                `order`.total_price AS total_price,
                order_item_status.`name` AS `status`
        """

        extra_sql = """
            FROM order_items AS order_item
                INNER JOIN orders AS `order` 
                    ON order_item.order_id = `order`.id
                INNER JOIN products AS product 
                    ON order_item.product_id = product.id
                INNER JOIN sellers AS seller 
                    ON product.seller_id = seller.account_id
                INNER JOIN stocks AS stock 
                    ON order_item.stock_id = stock.id
                INNER JOIN colors AS color 
                    ON stock.color_id = color.id
                INNER JOIN sizes AS size 
                    ON stock.size_id = size.id
                INNER JOIN order_item_status_types AS order_item_status 
                    ON order_item.order_item_status_type_id = order_item_status.id
            WHERE
                order_item.is_deleted = 0
                AND order_item_status.id = %(status)s
        """

        # 검색 권한 조건
        if data["permission"] == 2:
            extra_sql += "AND seller.account_id = %(account)s"

        # 검색어 조건
        if data['number']:
            extra_sql += " AND `order`.order_number = %(number)s"
        if data['detail_number']:
            extra_sql += " AND order_items.order_detail_number = %(detail_number)s"
        if data['sender_name']:
            extra_sql += " AND `order`.sender_name = %(sender_name)s"
        if data['sender_phone']:
            extra_sql += " AND `order`.sender_phone = %(sender_phone)s"
        if data['seller_name']:
            extra_sql += " AND seller.`name` = %(seller_name)s"
        if data['product_name']:
            extra_sql += " AND product.`name` LIKE %(product_name)s"

        # 날짜 조건
        if data['start_date'] and data['end_date']:
            extra_sql += """ AND order_item.updated_at BETWEEN CONCAT(%(start_date)s, ' 00:00:00') AND CONCAT(%(end_date)s, ' 23:59:59')
            """

        # 셀러 속성 조건
        if data['attributes']:
            extra_sql += " AND seller.seller_attribute_type_id IN %(attributes)s"

        # 정렬 조건
        if data['status'] == 1:
            if data['order_by'] == 'recent':
                extra_sql += " ORDER BY order_item.id DESC"
            else:
                extra_sql += " ORDER BY order_item.id ASC"
        else:
            if data['order_by'] == 'recent':
                extra_sql += " ORDER BY order_item.updated_at DESC"
            else:
                extra_sql += " ORDER BY order_item.updated_at ASC"

        total_count_sql += extra_sql
        sql += extra_sql

        # 페이지 조건
        sql += " LIMIT %(page)s, %(length)s;"
        print(sql)

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            list = cursor.fetchall()
            print(list)
            if not list:
                raise OrderDoesNotExist('order does not exist')
            cursor.execute(total_count_sql, data)
            count = cursor.fetchall()

            return {'total_count': count[0]['total_count'], 'order_lists': list}
        # except Exception:
        #     traceback.print_exc()
        #     raise ServerError('server_error')


    def update_order_status_dao(self, connection, data):
        sql = """
            UPDATE order_items
            SET order_item_status_type_id = %(new_status)s
            WHERE id IN %(ids)s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            affected_row = cursor.execute(sql, data)
            if affected_row == 0:
                raise UnableToUpdate('unable to update status')

    def add_order_history_dao(self, connection, update_data):
        sql = """
            INSERT
            INTO order_item_histories (order_item_id, order_item_status_type_id, updater_id)
            VALUES (%s, %s, %s);
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            created_rows = cursor.executemany(sql, update_data)
            if created_rows == 0:
                raise UnableToUpdate('unable to update status')


class OrderDetailDao():
    """ Persistence Layer

        Attributes: None

        Author: 김민서

        History:
            2021-01-01(김민서): 초기 생성
    """

    def get_order_info_dao(self, connection, order_item_id):
        sql = """
            SELECT 
                `order`.id AS order_id, 
                `order`.order_number AS order_number,
                `order`.created_at AS order_purchased_date,
                `order`.total_price AS total_price
            FROM order_items AS order_item
                INNER JOIN orders AS `order` 
                    ON order_item.order_id = `order`.id
                INNER JOIN delivery_memo_types AS delivery_memo
                    ON `order`.delivery_memo_type_id = delivery_memo.id
                INNER JOIN products AS product 
                    ON order_item.product_id = product.id
                INNER JOIN sellers AS seller 
                    ON product.seller_id = seller.account_id
                INNER JOIN stocks AS stock 
                    ON order_item.stock_id = stock.id
                INNER JOIN colors AS color 
                    ON stock.color_id = color.id
                INNER JOIN sizes AS size 
                    ON stock.size_id = size.id
                INNER JOIN order_item_status_types AS order_item_status 
                    ON order_item.order_item_status_type_id = order_item_status.id
            WHERE order_item.id = %s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, order_item_id)
            result = cursor.fetchall()
            if not result:
                return DoesNotOrderDetail('does not exist order detail')
            return result


    def get_order_detail_info_dao(self, connection, order_item_id):
        sql = """
            SELECT 
                order_item.id AS order_item_id,
                order_item.order_detail_number AS order_detail_number,
                order_item_status.`name` AS status,
                order_item.created_at AS order_item_purchased_date,
                `order`.sender_phone AS customer_phone
            FROM order_items AS order_item
                INNER JOIN orders AS `order` 
                    ON order_item.order_id = `order`.id
                INNER JOIN delivery_memo_types AS delivery_memo
                    ON `order`.delivery_memo_type_id = delivery_memo.id
                INNER JOIN products AS product 
                    ON order_item.product_id = product.id
                INNER JOIN sellers AS seller 
                    ON product.seller_id = seller.account_id
                INNER JOIN stocks AS stock 
                    ON order_item.stock_id = stock.id
                INNER JOIN colors AS color 
                    ON stock.color_id = color.id
                INNER JOIN sizes AS size 
                    ON stock.size_id = size.id
                INNER JOIN order_item_status_types AS order_item_status 
                    ON order_item.order_item_status_type_id = order_item_status.id
            WHERE order_item.id = %s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, order_item_id)
            result = cursor.fetchall()
            if not result:
                return DoesNotOrderDetail('does not exist order detail')
            return result


    def get_product_info_dao(self, connection, order_item_id):
        sql = """
            SELECT 
                product.product_code AS product_number,
                product.`name` AS product_name,
                CONCAT(order_item.original_price ,' 원 (할인가 ', order_item.discounted_price, '원)') AS price,
                order_item.sale AS discount_rate,
                seller.`name` AS brand_name,
                CONCAT(color.`name`, '/', size.`name`) AS option_information,
                order_item.quantity AS qauntity
            FROM order_items AS order_item 
                INNER JOIN orders AS `order` 
                    ON order_item.order_id = `order`.id
                INNER JOIN delivery_memo_types AS delivery_memo
                    ON `order`.delivery_memo_type_id = delivery_memo.id
                INNER JOIN products AS product 
                    ON order_item.product_id = product.id
                INNER JOIN sellers AS seller 
                    ON product.seller_id = seller.account_id
                INNER JOIN stocks AS stock 
                    ON order_item.stock_id = stock.id
                INNER JOIN colors AS color 
                    ON stock.color_id = color.id
                INNER JOIN sizes AS size 
                    ON stock.size_id = size.id
                INNER JOIN order_item_status_types AS order_item_status 
                    ON order_item.order_item_status_type_id = order_item_status.id
            WHERE order_item.id = %s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, order_item_id)
            result = cursor.fetchall()
            if not result:
                return DoesNotOrderDetail('does not exist order detail')
            return result


    def get_recipient_info_dao(self, connection, order_item_id):
        sql = """
            SELECT 
                `order`.user_id AS user_id,
                `order`.sender_name AS customer_name,
                `order`.recipient_name AS recipient_name,
                `order`.recipient_phone AS recipient_phone,
                CONCAT(`order`.address1, ' ', `order`.address2, ' (', `order`.post_number, ')') AS destination,
                delivery_memo.content AS delivery_memo
            FROM order_items AS order_item
                INNER JOIN orders AS `order` 
                    ON order_item.order_id = `order`.id
                INNER JOIN delivery_memo_types AS delivery_memo
                    ON `order`.delivery_memo_type_id = delivery_memo.id
                INNER JOIN products AS product 
                    ON order_item.product_id = product.id
                INNER JOIN sellers AS seller 
                    ON product.seller_id = seller.account_id
                INNER JOIN stocks AS stock
                    ON order_item.stock_id = stock.id
                INNER JOIN colors AS color 
                    ON stock.color_id = color.id
                INNER JOIN sizes AS size 
                    ON stock.size_id = size.id
                INNER JOIN order_item_status_types AS order_item_status 
                    ON order_item.order_item_status_type_id = order_item_status.id
            WHERE order_item.id = %s;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, order_item_id)
            result = cursor.fetchall()
            if not result:
                return DoesNotOrderDetail('does not exist order detail')
            return result


    def get_order_status_history_info_dao(self, connection, order_item_id):
        sql = """
            SELECT 
                order_item_history.created_at AS `date`,
                order_item_status.`name` AS `status`
            FROM order_item_histories AS order_item_history
                JOIN order_item_status_types AS order_item_status
                    ON order_item_history.order_item_status_type_id = order_item_status.id
            WHERE 
                order_item_history.order_item_id = %s
            ORDER BY order_item_history.id DESC;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, order_item_id)
            result = cursor.fetchall()
            if not result:
                return DoesNotOrderDetail('does not exist order detail')
            return result


    def get_updated_time_dao(self, connection, order_item_id):
        sql = """
            SELECT orders.updated_at
            FROM orders 
                INNER JOIN order_items
                    ON order_items.order_id = orders.id 
            WHERE order_items.id = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, order_item_id)
            result = cursor.fetchone()
            return result


    def update_sender_phone_dao(self, connection, data):
        sql = """
            UPDATE orders 
            INNER JOIN order_items 
                ON orders.id = order_items.order_id
            SET sender_phone = %(sender_phone)s
            WHERE order_items.id = %(order_item_id)s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                affect_row = cursor.execute(sql, data)
                if affect_row == 0:
                    raise DeniedUpdate('denied to update')
        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')


    def update_recipient_phone_dao(self, connection, data):
        sql = """
            UPDATE orders 
            INNER JOIN order_items 
                ON orders.id = order_items.order_id
            SET recipient_phone = %(recipient_phone)s 
            WHERE order_items.id = %(order_item_id)s;
        """
        print('a')
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                affect_row = cursor.execute(sql, data)
                print(affect_row)
                if affect_row == 0:
                    raise DeniedUpdate('denied to update')
        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')


    def update_address_dao(self, connection, data):
        sql = """
        UPDATE orders
        INNER JOIN order_items ON orders.id = order_items.order_id
        SET address1 = %(address1)s, address2 = %(address2)s
        WHERE order_items.id = %(order_item_id)s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                affect_row = cursor.execute(sql, data)
                if affect_row == 0:
                    raise DeniedUpdate('denied to update')
        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')






