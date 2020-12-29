import pymysql
from utils.custom_exceptions import EventDoesNotExist

class EventDao:
    """ Persistence Layer

        Attributes: None

        Author: 강두연

        History:
            2020-12-28(강두연): 초기 생성 및 조회 기능 작성
            2020-12-29(강두연): 이벤트 검색조건별 조회 작성
    """
    def get_events_list(self, connection, data):
        """기획전 정보 조회

            Args:
                connection: 데이터베이스 연결 객체
                data   : 비지니스 레이어에서 넘겨 받은 검색 조건 키벨류

            Author: 강두연

            Returns:
                return [
                    {
                        "created_at": "Mon, 28 Dec 2020 16:40:41 GMT",
                        "end_date": "Mon, 01 Mar 2021 00:00:00 GMT",
                        "event_kind": "버튼",
                        "event_name": "성보의 하루 시리즈2(버튼형)",
                        "event_number": 2,
                        "event_status": "진행중",
                        "event_type": "상품(이미지)",
                        "is_display": "노출",
                        "product_count": 59,
                        "start_date": "Mon, 19 Oct 2020 00:00:00 GMT"
                    },
                    {
                        "created_at": "Mon, 28 Dec 2020 16:40:41 GMT",
                        "end_date": "Mon, 01 Mar 2021 00:00:00 GMT",
                        "event_kind": "상품",
                        "event_name": "성보의 하루 시리즈",
                        "event_number": 1,
                        "event_status": "진행중",
                        "event_type": "상품(이미지)",
                        "is_display": "노출",
                        "product_count": 40,
                        "start_date": "Mon, 19 Oct 2020 00:00:00 GMT"
                    }
                ]

            History:
                2020-12-28(강두연): 초기 생성 및 조회 기능 작성
                2020-12-29(강두연): 이벤트 검색조건별 조회 작성

            Raises:
                404, {'message': 'event not exist', 'errorMessage': 'event does not exist'} : 이벤트 정보 조회 실패
        """

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

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if not result:
                raise EventDoesNotExist('event does not exist')
            return result
