from utils.custom_exceptions import (OrderFilterNotExist,
                                     NoPermission,
                                     DateInputDoesNotExist,
                                     NotAllowedStatus,
                                     InputDoesNotExist,
                                     UnableUpdateAddress,
                                     UnableToUpdate
                                     )


class OrderService:
    """ Business Layer
            Attributes:
                get_order_list_dao: OrderDao 클래스

            Author: 김민서

            History:
                2020-12-29(김민서): 초기 생성
                2020-12-30(김민서): 1차 수정
                2020-12-31(김민서): 2차 수정
    """
    def __init__(self, admin_order_dao):
        self.admin_order_dao = admin_order_dao

    def get_orders_service(self, connection, data):
        try:
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('no_permission')

            if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
                raise DateInputDoesNotExist('must_be_other_date_input')

            if data['start_date'] and data['end_date'] and data['number'] and data['detail_number'] and data['sender_name'] \
                      and data['sender_phone'] and data['seller_name'] and data['product_name']:
                raise OrderFilterNotExist('must_be_date_inputs_or_filter_inputs')

            data['length'] = int(data['length'])
            data['page'] = (data['page'] - 1) * data['length']

            if data['sender_phone']:
                data['sender_phone'] = data['sender_phone'].replace("-", "")
            if data['product_name']:
                data['product_name'] = '%' + data['product_name'] + '%'

            return self.admin_order_dao.get_order_list_dao(connection, data)

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

            self.admin_order_dao.update_order_status_dao(connection, data)
            self.admin_order_dao.add_order_history_dao(connection, update_data)

        except KeyError:
            return 'key_error'


    def get_order_detail_service(self, connection, data):
        try:
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('no_permission')
            order_item_id = data["order_item_id"]

            order_info           = self.admin_order_dao.get_order_info_dao(connection, order_item_id)
            order_detail_info    = self.admin_order_dao.get_order_detail_info_dao(connection, order_item_id)
            product_info         = self.admin_order_dao.get_product_info_dao(connection, order_item_id)
            recipient_info       = self.admin_order_dao.get_recipient_info_dao(connection, order_item_id)
            order_status_history = self.admin_order_dao.get_order_status_history_info_dao(connection, order_item_id)
            updated_at_time      = self.admin_order_dao.get_updated_time_dao(connection, order_item_id)[0]

            return {
                "order_info": order_info,
                "order_detail_info": order_detail_info,
                "product_info": product_info,
                "recipient_info": recipient_info,
                "order_status_history": order_status_history,
                "updated_at_time": updated_at_time
            }

        except KeyError:
            return 'key_error'


    def update_order_detail_service(self, connection, data):
        try:
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('no_permission')

            order_item_id = data['order_item_id']
            updated_at_time = data['updated_at_time']
            sender_phone = data['sender_phone']
            recipient_phone = data['recipient_phone']
            address1 = data['address1']
            address2 = data['address2']

            if (sender_phone and recipient_phone and address1 and address2) in data:
                raise InputDoesNotExist('input_does_not_exists')

            if (not address1 and address2) or (not address2 and address1):
                raise UnableUpdateAddress('one_of_address_inputs_does_not_exist')

            time = self.admin_order_dao.get_updated_time_dao(connection, order_item_id)
            time = time[0].strftime("%Y-%m-%d %H:%M:%S")

            if time != updated_at_time:
                raise UnableToUpdate('unable_to_update')

            if address1 and address2:
                self.admin_order_dao.update_address_dao(connection, data)

            if sender_phone:
                data = {'order_item_id': order_item_id, 'sender_phone': sender_phone}
                self.admin_order_dao.update_sender_phone_dao(connection, data)

            if recipient_phone:
                data = {'order_item_id': order_item_id, 'recipient_phone': recipient_phone}
                self.admin_order_dao.update_recipient_phone_dao(connection, data)

        except KeyError:
            return 'key_error'