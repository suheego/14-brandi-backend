from utils.custom_exceptions import CustomerPermissionDenied, CheckoutDenied


class StoreOrderService:
    """ Business Layer

        Attributes:
            order_dao: OrderDao 클래스

        Author: 고수희

        History:
            2020-12-30(고수희): 초기 생성
    """

    def __init__(self, order_dao):
        self.order_dao = order_dao

    def get_order_service(self, connection, data):
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
            403, {'message': 'key error',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 없음
        History:
            2020-12-30(고수희): 초기 생성
        """
        try:
            #사용자의 권한 체크
            permission_check = self.order_dao.get_user_permission_check_dao(connection, data)
            if permission_check['permission_type_id'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

        except KeyError:
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
            400, {'message': 'unable to create',
            'errorMessage': 'unable_to_create'} : 장바구니 상품 추가 실패
            403, {'message': 'key error',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 없음
        History:
            2020-12-30(고수희): 초기 생성
        """

        try:
            #사용자 권한 체크
            permission_check = self.cart_item_dao.get_user_permission_check_dao(connection, data)
            if permission_check['permission_type_id'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            #상품 구매 가능 여부 체크
            if data['sold_out'] == "true":
                raise CheckoutDenied('unable_to_checkout')

            #상품 품절 여부 체크
            sold_out = self.order_dao.product_soldout_dao(connection, data)
            if sold_out['sold_out'] is True:
                raise CheckoutDenied('unable_to_checkout')

            #배송 정보 추가 (배송 메모가 직접 입력일 경우)
            if data['delivery_memo_type_id'] == 5:
                custom_memo = self.order_dao.post_delivery_type_dao(connection, data)
                data['delivery_memo_type_id'] = custom_memo

            #주문 정보 추가 (주문자 정보, 배송지 정보, 기타 배송 정보)
            order = self.order_dao.post_order_dao(connection, data)

            #주문 상품 추가 (주문 상품에 대한 정보)
            self.order_dao.post_order_item_dao(connection, data)

            #주문 상품 정보 이력 추가
            self.order_dao.post_order_item_history_dao(connection, data)

            #주문 상품 타입 추가
            self.order_dao.post_order_item_status_dao(connection, data)

            #주문한 상품 수량 만큼 상품 판매량 추가
            self.order_dao.post_product_sales_rate_dao(connection, data)

            #주문한 상품 수량 만큼 재고 감소 처리
            self.order_dao.patch_product_remain_dao(connection, data)

            #장바구니 상품 논리 삭제 처리
            self.order_dao.is_delete_cart_item_dao(connection, data)

            #주문자 정보 추가/수정
            cart_item = self.order_dao.custmer_information_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')
