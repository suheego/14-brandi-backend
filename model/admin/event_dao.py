import pymysql


class EventDao:
    def get_events_list(self, connection, data):
        sql = """
            SELECT
                `event`.id AS event_number
                , `event`.`name` AS event_name
                , CASE WHEN NOW() BETWEEN `event`.start_date AND `event`.end_date THEN '진행중'
                     WHEN NOW() < `event`.start_date THEN '대기'
                     ELSE '종료' END AS event_status
                , event_type.`name` AS event_type
                , event_kind.`name` AS event_kind
                , `event`.start_date AS start_date
                , `event`.end_date AS end_date
                , CASE WHEN `event`.is_display = 0 THEN '비노출' ELSE '노출' END AS is_display
                , `event`.created_at AS created_at
                , (SELECT COUNT(CASE WHEN events_products.event_id = `event`.id THEN 1 END)
                    FROM events_products) AS product_count
            FROM `events` AS `event`
                INNER JOIN event_types AS event_type
                    ON `event`.event_type_id = event_type.id
                INNER JOIN event_kinds AS event_kind
                   ON `event`.event_kind_id = event_kind.id
            WHERE
                `event`.is_deleted = 0
        """

        search_query = {
            'event_name': ' AND `event`.`name` LIKE %(name)s',
            'event_number': ' AND `event`.id = %(number)s',
            'progress': ' AND NOW() BETWEEN `event`.start_date AND `event`.end_date',
            'wait': ' AND NOW() < `event`.start_date',
            'end': '  AND NOW() > `event`.end_date',
            'event_crated': """
                 AND `event`.created_at BETWEEN 
                CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """,
            'display': ' AND `event`.is_display = 1',
            'not_display': ' AND `event`.is_display = 0'
        }

        order_query = {
            'desc': ' ORDER BY `event`.id DESC'
        }

        limit_query = ' LIMIT %(page)s, %(length)s;'

        # search option 1 : search by keyword (event_name or event_number)
        print(data)
        if data['name']:
            sql += search_query['event_name']
        elif data['number']:
            sql += search_query['event_number']

        # search option 2 : search by event_status
        if data['status']:
            sql += search_query[data['status']]

        # search option 3 : exposure
        if data['exposure'] is not None and data['exposure']:
            sql += search_query['display']
        elif data['exposure'] is not None and not data['exposure']:
            sql += search_query['not_display']

        # search option 4 : event_registered_date
        if data['start_date'] and data['end_date']:
            sql += search_query['event_crated']

        sql += order_query['desc'] + limit_query
        # print(sql)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            print(result)
            if not result:
                print('no result')
                # error handling required!
            return result
