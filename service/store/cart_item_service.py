from utils.custom_exceptions import CustomerPermissionDenied


class CartItemService:
    """ Business Layer

        Attributes:
            cart_item_dao: CartItemDao 클래스

        Author: 고수희

        History:
            2020-12-28(고수희): 초기 생성
    """

    def __init__(self, cart_item_dao):
        self.cart_item_dao = cart_item_dao

    def get_cart_item_service(self, connection, data):
        """ GET 메소드: 장바구니 상품 조회

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 빈값 반환

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            403, {'message': 'key error',
            'errorMessage': 'customer_permission_denied'} : 잘못 입력된 키값

        History:
            2020-12-28(고수희): 초기 생성
        """
        try:
            permission_check = data['user_id']
            if permission_check != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            return self.cart_item_dao.get_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')

    def post_cart_item_service(self, connection, data):
        """ POST 메소드: 장바구니 상품 추가, 동일한 상품 옵션이 이미 있을 경우 상품 수량 수정

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 빈값 반환

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값

        History:
            2020-12-28(고수희): 초기 생성
        """

        try:
            # #동일한 상품 및 상품 옵션 중복 검사
            # item_exist = self.cart_item_dao.patch_dao(connection, data)
            # if item_exist:
            #     return self.cart_item_dao.patch_dao(connection, data)

            return self.cart_item_dao.post_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')
