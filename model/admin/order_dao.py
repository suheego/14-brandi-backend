import pymysql
from utils.custom_exceptions import OrderDoesNotExist, UnableToUpdate


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
            extra_sql += " AND order_item.updated_at BETWEEN CONCAT(%(start_date)s, ' 00:00:00') AND CONCAT(%(end_date)s, ' 23:59:59')"

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

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            list = cursor.fetchall()
            if not list:
                raise OrderDoesNotExist('order does not exist')
            cursor.execute(total_count_sql, data)
            count = cursor.fetchall()

            return {'total_count': count[0]['total_count'],'order_lists': list}


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