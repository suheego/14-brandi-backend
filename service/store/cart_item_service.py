from utils.custom_exceptions import CustomerPermissionDenied, CartItemCreateFail


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
        """ GET 메소드: 장바구니 상품 조회, 조회 시 상품 품절 여부 체크

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
            'errorMessage': 'customer_permission_denied'} : 잘못 입력된 키값

        History:
            2020-12-28(고수희): 초기 생성
        """
        try:
            #사용자의 권한 체크
            permission_check = self.cart_item_dao.get_user_permission_check_dao(connection, data)
            if permission_check['permission_type_id'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            #상품 품절 여부 체크
            sold_out = self.cart_item_dao.get_cart_item_soldout_dao(connection, data)

            #상품 정보 조회
            cart_item = self.cart_item_dao.get_dao(connection, data)

            # 상품 정보 조회에 상품 품절 여부 결과 병합하여 리턴
            cart_item.update(sold_out)
            return cart_item

        except KeyError:
            raise KeyError('key_error')

    def post_cart_item_service(self, connection, data):
        """ POST 메소드: 장바구니 상품 추가

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

        History:
            2020-12-28(고수희): 초기 생성
        """

        try:
            #사용자 권한 체크
            permission_check = self.cart_item_dao.get_user_permission_check_dao(connection, data)
            if permission_check['permission_type_id'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            #장바구니에 담을 상품이 재고가 있는지 체크
            sold_out = self.cart_item_dao.product_soldout_dao(connection, data)
            if sold_out['soldOut'] is True:
                raise CartItemCreateFail('unable_to_create')
            return self.cart_item_dao.post_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')
