class EventService:

    def __init__(self, event_dao):
        self.event_dao = event_dao

    def get_events_service(self, connection):
        try:
            return self.event_dao.get_events_list(connection)

        except Exception as e:
            raise e
