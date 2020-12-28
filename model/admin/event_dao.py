import pymysql


class EventDao:
    def get_events_list(self, connection):
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
            ORDER BY 
                `event`.id DESC
            LIMIT 0, 10;
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            if not result:
                print('no result')
                # error handling required!
            return result
