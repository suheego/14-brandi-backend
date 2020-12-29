class DestinationSelectService:

    def __init__(self, destination_dao):
        self.destination_dao = destination_dao

    def destination_select_service(self, connection, data):
        return self.destination_dao.select_destination(connection, data)

    def create_destination_service(self, connection, data):
        try:
            permission_type = self.destination_dao.check_account_type(data['user_id'])
            if permission_type == 1:
                pass
            if permission_type == 2:
                pass
            return self.destination_dao.create_destination_dao(connection, data)
        except KeyError:
            raise KeyError('key_error')
