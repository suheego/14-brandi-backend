from utils.custom_exceptions import (OrderFilterNotExist,
                                     NoPermission,
                                     DateInputDoesNotExist,
                                     NotAllowedStatus,
                                     )


class OrderService:
    """ Business Layer
            Attributes:
                get_order_list_dao: OrderDao 클래스

            Author: 김민서

            History:
                2020-20-29(김민서): 초기 생성
                2020-12-30(김민서): 1차 수정
                2020-12-31(김민서): 2차 수정
    """
    def __init__(self, master_order_dao):
        self.master_order_dao = master_order_dao


    def get_orders_service(self, connection, data):
        try:
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('no_permission')

            if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
                raise DateInputDoesNotExist('must_be_other_date_input')

            filters = data['start_date'] + data['end_date'] + data['number'] + data['detail_number'] + data['sender_name'] \
                      + data['sender_phone'] + data['seller_name'] + data['product_name']

            if not filters:
                raise OrderFilterNotExist('must_be_date_inputs_or_filter_inputs')

            data['page'] = (data['page'] - 1) * data['length']
            if data['sender_phone']:
                data['sender_phone'] = data['sender_phone'].replace("-", "")
            if data['product_name']:
                data['product_name'] = '%' + data['product_name'] + '%'

            return self.master_order_dao.get_order_list_dao(connection, data)

        except KeyError:
            return 'key_error'


    def update_order_status_service(self, connection, data):
        try:
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('no_permission')

            if not (data['status'] == 1 or data['status'] == 2):
                raise NotAllowedStatus('now_order_status_is_not_allowed_to_update_status')

            data['new_status'] = data['status'] + 1
            update_data = [[id, data['new_status'], data['account']] for id in data['ids']]

            self.master_order_dao.update_order_status_dao(connection, data)
            self.master_order_dao.add_order_history_dao(connection, update_data)

        except KeyError:
            return 'key_error'
