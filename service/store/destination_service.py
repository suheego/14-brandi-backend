class DestinationSelectService:

    def __init__(self, destination_dao):
        self.destination_dao = destination_dao

    def destination_select_service(self, connection, data):
        return self.destination_dao.select_destination(connection, data)

    def create_destination_service(self, connection, data):
        return self.destination_dao.create_destination_dao(connection, data)


