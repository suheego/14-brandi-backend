import traceback
from utils.custom_exceptions import CustomerPermissionDenied, CheckoutDenied


class StoreOrderService:
    """ Business Layer

        Attributes:
            store_order_dao: StoreOrderDao 클래스

        Author: 고수희

        History:
            2020-12-30(고수희): 초기 생성
    """

    def __init__(self, store_order_dao):
        self.store_order_dao = store_order_dao

    def get_store_order_service(self, connection, data):
        """ GET 메소드: 결제 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 조회한 상품 정보와 상품 품절 여부 반환

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'order does not exist',
            'errorMessage': 'order_does_not_exist'} : 결제 상품 정보 조회 실패
            403, {'message': 'customer permission denied',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 없음

        History:
            2020-12-30(고수희): 초기 생성
        """
        try:
            #사용자의 권한 체크
            if data['user_permissions'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            #상품 결제 완료 결과 조회
            return self.store_order_dao.get_store_order_dao(connection, data)

        except KeyError:
            traceback.print_exc()
            raise KeyError('key_error')

    def post_order_service(self, connection, data):
        """ POST 메소드: 결제 추가

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 추가완료 된 장바구니 id 반환

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'product does not exist',
            'errorMessage': 'product_does_not_exist'} : 상품을 조회할 수 없음
            400, {'message': 'delivery memo create denied',
            'errorMessage': 'unable_to_create'} : 배송 정보 추가 실패
            400, {'message': 'order create denied',
            'errorMessage': 'unable_to_create'} : 주문 정보 추가 실패
            400, {'message': 'order item create denied',
            'errorMessage': 'unable_to_create'} : 주문 상품 추가 실패
            400, {'message': 'order history create denied',
            'errorMessage': 'unable_to_create'} : 주문 상품 정보 이력 추가 실패
            400, {'message': 'product remain update denied',
            'errorMessage': 'unable_to_update'} : 상품 재고 업데이트 실패
            400, {'message': 'invalid_delete_command_access',
            'errorMessage': 'unable_to_delete'} : 논리삭제 실패
            403, {'message': 'customer permissions denied',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 없음
            500, {'message: server_error',
            'errorMessage': 'server_error'} :서버 에러 발생

        History:
            2020-12-30(고수희): 초기 생성
        """

        try:
            #사용자 권한 체크
            if data['user_permission'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            #상품 구매 가능 여부 체크
            if data['sold_out'] is True:
                raise CheckoutDenied('unable_to_checkout')

            #상품 품절 여부 체크
            sold_out = self.store_order_dao.order_product_soldout_dao(connection, data)
            if sold_out['sold_out'] is True:
                raise CheckoutDenied('unable_to_checkout')

            #배송 정보 추가 (배송 메모가 직접 입력일 경우)
            if data['delivery_memo_type_id'] == 5:
                custom_memo = self.store_order_dao.post_delivery_type_dao(connection, data)
                data['delivery_memo_type_id'] = custom_memo

            #주문번호 생성을 위한 당일 주문량 파악
            today = self.store_order_dao.get_today_order_number_dao(connection)
            data.update(today)

            #주문 정보 추가 (주문자 정보, 배송지 정보, 기타 배송 정보)
            order = self.store_order_dao.post_store_order_dao(connection, data)
            data['order_id'] = order
            data['order_item_status_type_id'] = 1

            #주문 상품 추가 (주문 상품에 대한 정보)
            self.store_order_dao.post_store_order_item_dao(connection, data)

            #주문 상품 정보 이력 추가
            self.store_order_dao.post_store_order_item_history_dao(connection, data)

            #주문한 상품 수량 만큼 재고 감소 처리
            self.store_order_dao.patch_product_remain_dao(connection, data)

            #장바구니 상품 논리 삭제 처리
            self.store_order_dao.patch_is_delete_cart_item_dao(connection, data)

            #주문자 정보가 없으면 주문자 정보 추가, 있으면 수정
            self.store_order_dao.patch_customer_information_dao(connection, data)

            return order

        except KeyError:
            traceback.print_exc()
            raise KeyError('key_error')
