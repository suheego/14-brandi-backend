from utils.custom_exceptions import UserAlreadyExist

class OrderService:
    def __init__(self, master_order_dao):
        self.master_order_dao = master_order_dao

    def get_prepare_product_service(self, connection, data):
        try:
            if data['sender_phone']:
                data['sender_phone'] = data['sender_phone'].replace("-", "")

            if data['product_name']:
                data['product_name'] = '%' + data['product_name'] + '%'

            #if not searchs and dates:
            #raise UserAlreadyExist('already_exist')

            return self.master_order_dao.get_order_list_dao(connection, data)

        except KeyError:
            return 'key_error'