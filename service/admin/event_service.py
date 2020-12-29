class EventService:
    """ Business Layer

        Attributes:
            event_dao: EventDao 클래스

        Author: 강두연

        History:
            2020-20-28(강두연): 초기 생성
            2020-20-21(강두연): 1차 수정
    """
    def __init__(self, event_dao):
        self.event_dao = event_dao

    def get_events_service(self, connection, data):
        try:
            data['page'] = (data['page']-1) * data['length']
            if data['name']:
                data['name'] = '%' + data['name'] + '%'
            return self.event_dao.get_events_list(connection, data)

        except Exception as e:
            raise e
