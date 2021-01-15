import traceback
from utils.custom_exceptions import CustomerPermissionDenied, CartItemCreateDenied


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
            403, {'message': 'customer permission denied',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 없음
        History:
            2020-12-28(고수희): 초기 생성
            2021-01-01(고수희): 로직 수정
        """
        try:
            #사용자의 권한 체크
            if data['user_permission'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            #상품 정보 조회
            return self.cart_item_dao.get_cart_item_dao(connection, data)

        except CustomerPermissionDenied as e:
            traceback.print_exc()
            raise e

        except KeyError:
            traceback.print_exc()
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
            403, {'message': 'customer permission denied',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 없음
        History:
            2020-12-28(고수희): 초기 생성
            2021-01-02(고수희): 권한 체크 수정
        """

        try:
            #사용자 권한 체크
            if data['user_permission'] != 3:
                raise CustomerPermissionDenied('customer_permission_denied')

            #장바구니에 담을 상품이 재고가 있는지 체크
            sold_out = self.cart_item_dao.product_soldout_dao(connection, data)
            if sold_out['soldout'] is True:
                raise CartItemCreateDenied('unable_to_create')
            return self.cart_item_dao.post_cart_item_dao(connection, data)

        except CustomerPermissionDenied as e:
            traceback.print_exc()
            raise e

        except CartItemCreateDenied as e:
            traceback.print_exc()
            raise e

        except KeyError:
            traceback.print_exc()
            raise KeyError('key_error')
