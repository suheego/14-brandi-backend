class EventService:

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
