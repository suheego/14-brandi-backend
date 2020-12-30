
import pymysql
from utils.custom_exceptions import UserUpdateDenied, UserCreateDenied, UserNotExist


class OrderListDao:
    def get_order_list_dao(self, connection, data):
        sql = """
            SELECT order_item.id,
                order_item.created_at AS purchased_date,
                order_item.updated_at AS updated_at,
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
                order_item_status.id = %(order_item_status_type_id)s
                AND order_item.is_deleted = 0
        """


        # 검색어 조건
        if data['order_number']:
            sql += " AND `order`.order_number = %(order_number)s"
        if data['order_detail_number']:
            sql += " AND order_items.order_detail_number = %(order_detail_number)s"
        if data['sender_name']:
            sql += " AND `order`.sender_name = %(sender_name)s"
        if data['sender_phone']:
            sql += " AND `order`.sender_phone = %(sender_phone)s"
        if data['seller_name']:
            sql += " AND seller.`name` = %(seller_name)s"
        if data['product_name']:
            sql += " AND product.`name` LIKE %%(product_name)s%"

        # 날짜 조건
        if data['start_date'] and data['end_date']:
            sql += " AND order_item.updated_at BETWEEN CONCAT(%(start_date)s, ' 00:00:00') AND CONCAT(%(end_date)s, ' 23:59:59')"

        # 셀러 속성 조건
        if data['seller_attribute_type_ids'] != ['']:
            for type_id in data['seller_attribute_type_ids']:
                sql += f" OR seller.seller_attribute_type_id = {type_id}"

        # 정렬 조건
        if not (data['g'] and data['order_by']):
            sql += " ORDER BY order_item.created_at DESC"
        else:
            sql += f" ORDER BY order_item.{data['g']} {data['order_by']}"


        # 페이지
        if not (data['offset'] and data['limit']):

            sql += " LIMIT 0, 50;"
        else:

            sql += f" LIMIT {data['offset']}, {data['limit']};"


        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            return result

    def patch_order_status_dao(self, connection, status_id):


