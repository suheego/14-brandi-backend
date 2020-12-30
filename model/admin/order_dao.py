import pymysql
from utils.custom_exceptions import UserUpdateDenied, UserCreateDenied, UserNotExist


class OrderDao:
    """ Persistence Layer

            Attributes: None

            Author: 김민

            History:
                2020-2012-29(김민서): 초기 생성
                2020-12-30(김민서): 1차 수정
    """
    def get_order_list_dao(self, connection, data):
        """주문 리스 조회

                Args:
                    connection: 데이터베이스 연결 객체
                    user_id   : 서비스 레이어에서 넘겨 받은 수정할 user_id

                Author: 김민서

                Returns:
                    return [{'id': 12, 'name': '김기용', 'gender': '남자', 'age': '18'}]

                History:
                    2020-12-29(김민서): 초기 생성
                    2020-12-30(김민서): 1차 수정

                Raises:
                    400, {'message': 'user dose not exist', 'errorMessage': 'user_does_not_exist'} : 유저 정보 조회 실패
                """
        sql = """
            SELECT 
                order_item.id,
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
                order_item_status.id = %(status)s
                AND order_item.is_deleted = 0
        """

        seller_sql = """
            SELECT 
                order_item.id, 
                order_item.created_at AS purchased_date, 
                `order`.order_number AS order_number, 
                order_item.order_detail_number AS order_detail_number, 
                product.`name` AS product_name, 
                CONCAT(color.`name`, '/', size.`name`) AS option_information, 
                order_item.quantity AS quantity,
                `order`.sender_name AS customer_name,
                `order`.sender_phone AS customer_phone, 
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
                order_item_status.id = %(status)s
                AND seller.account_id = %(account)s
                AND order_item.is_deleted = 0
        """

        # sql문 설정
        if data['account']:
            sql = seller_sql

        # 검색어 조건
        if data['number']:
            sql += " AND `order`.order_number = %(number)s"
        if data['detail_number']:
            sql += " AND order_items.order_detail_number = %(detail_number)s"
        if data['sender_name']:
            sql += " AND `order`.sender_name = %(sender_name)s"
        if data['sender_phone']:
            sql += " AND `order`.sender_phone = %(sender_phone)s"
        if data['seller_name']:
            sql += " AND seller.`name` = %(seller_name)s"
        if data['product_name']:
            sql += " AND product.`name` LIKE %(product_name)s"

        # 날짜 조건
        if data['start_date'] and data['end_date']:
            sql += " AND order_item.updated_at BETWEEN CONCAT(%(start_date)s, ' 00:00:00') AND CONCAT(%(end_date)s, ' 23:59:59')"

        # 셀러 속성 조건
        if data['seller_attributes']:
            sql += " AND seller.seller_attribute_type_id IN %(seller_attributes)s"

        # 정렬
        if data['status'] == 1:
            if data['order_by'] == 'recent':
                sql += " ORDER BY order_item.id DESC"
            else:
                sql += " ORDER BY order_item.id ASC"
        else:
            if data['order_by'] == 'recent':
                sql += " ORDER BY order_item.updated_at DESC"
            else:
                sql += " ORDER BY order_item.updated_at ASC"

        # 페이지 조건 추가
        sql += " LIMIT %(page)s, %(length)s;"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            return result
