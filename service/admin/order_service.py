from utils.custom_exceptions import (OrderFilterNotExist,
                                     NoPermission,
                                     DateInputDoesNotExist,
                                     NotAllowedStatus,
                                     InputDoesNotExist,
                                     UnableUpdateAddress,
                                     UnableToUpdate,
                                     EndDateIsInvalid
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
            # 권한 체크
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('권한이 없습니다.')

            # 2개의 날짜 조건 모두 있는지 확인
            if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
                raise DateInputDoesNotExist('시작일과 마지막일이 모두 포함되어야 합니다.')

            # 시작일이 마지막일보다 더 늦는 경우
            if data['start_date'] > data['end_date']:
                raise EndDateIsInvalid("시작일이 마지막일보다 늦습니다.")

            # 날짜 조건과 검색어 조건 둘 중 하나의 조건은 반드시 필요
            if not(data['start_date'] or data['end_date'] or data['number'] or data['detail_number']
                    or data['sender_name'] or data['sender_phone'] or data['seller_name'] or data['product_name']):
                raise OrderFilterNotExist('검색어 조건과 날짜 조건 둘 중에 하나는 반드시 포함되어야 합니다.')

            # 주문 상태가 상품 준비 / 배송중 / 배송 완료 / 구매 확정 이 아닌 경우

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
            # 권한 조회 및 에러 처리
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('no permission')

            # 현재 주문 상태가 상품 준비 혹은 배송중이 아닌 경우 상태 업데이트 불가
            if not (data['status'] == 1 or data['status'] == 2):
                raise NotAllowedStatus('now order status is not allowed to update status')

            # 새로운 주문 상태 id 생성
            data['new_status'] = data['status'] + 1

            #
            update_data = [[id, data['new_status'], data['account']] for id in data['ids']]

            self.admin_order_dao.update_order_status_dao(connection, data)
            self.admin_order_dao.add_order_history_dao(connection, update_data)

        except KeyError:
            return 'key_error'


    def get_order_detail_service(self, connection, data):
        try:
            # 권한 조회 및 에러 처리
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('no permission')
            order_item_id = data["order_item_id"]

            # 주문 정보 조회
            order_info           = self.admin_order_dao.get_order_info_dao(connection, order_item_id)

            # 주문 상세 정보 조회
            order_detail_info    = self.admin_order_dao.get_order_detail_info_dao(connection, order_item_id)

            # 상품 정보 조회
            product_info         = self.admin_order_dao.get_product_info_dao(connection, order_item_id)

            # 수취자 정보 조회
            recipient_info       = self.admin_order_dao.get_recipient_info_dao(connection, order_item_id)

            # 주문 상태 변경 히스토리 조회
            order_status_history = self.admin_order_dao.get_order_status_history_info_dao(connection, order_item_id)

            # 최근 업데이트 시각 조회
            updated_at_time      = self.admin_order_dao.get_updated_time_dao(connection, order_item_id)[0]

            return {
                "order_info": order_info,
                "order_detail_info": order_detail_info,
                "product_info": product_info,
                "recipient_info": recipient_info,
                "order_status_history": order_status_history,
                "updated_at_time": updated_at_time
            }

        except Exception as e:
            raise e


    def update_order_detail_service(self, connection, data):
        try:
            # 권한 조회 및 에러 처리
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermission('no permission')

            order_item_id = data['order_item_id']
            updated_at_time = data['updated_at_time']
            sender_phone = data['sender_phone']
            recipient_phone = data['recipient_phone']
            address1 = data['address1']
            address2 = data['address2']

            # 수정 정보가 없는 경우 에러 처리
            if not (sender_phone or recipient_phone or address1 or address2):
                raise InputDoesNotExist('input does not exist')

            # 주소 정보와 상세 주소 정보 둘 중 하나가 없는 경우 에러 처리
            if (not address1 and address2) or (not address2 and address1):
                raise UnableUpdateAddress('one of address inputs does not exist')

            # 최근 업데이트 시각 정보 조회
            time = self.admin_order_dao.get_updated_time_dao(connection, order_item_id)
            time = time[0].strftime("%Y-%m-%d %H:%M:%S")

            # 최근 업데이트 시각과 다를 때 에러 처리
            if time != updated_at_time:
                raise UnableToUpdate('unable to update')

            # 주소와 상세주소 정보 수정
            if address1 and address2:
                self.admin_order_dao.update_address_dao(connection, data)

            # 주문자 번호 정보 수정
            if sender_phone:
                self.admin_order_dao.update_sender_phone_dao(connection, data)

            # 수취자 번호 정보 수정
            if recipient_phone:
                self.admin_order_dao.update_recipient_phone_dao(connection, data)

        except Exception as e:
            raise e