from utils.custom_exceptions import UserAlreadyExist

class OrderListService:
    def __init__(self, master_order_dao):
        self.master_order_dao = master_order_dao

    def get_prepare_product_service(self, connection, data):
        try:
            if data['sender_phone']:
                data['sender_phone'] = data['sender_phone'].replace("-", "")
            return self.master_order_dao.get_order_list_dao(connection, data)
        except KeyError:
            return 'key_error'

    def get_order_status_service(self, connection, status_id):
        try:

        except:
