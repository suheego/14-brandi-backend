from utils.custom_exceptions import UserAlreadyExist


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
        """유저의 카드에 담긴 상품를 가진 검색하 함수

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 홍길동

        Returns:
            return [{'id': 12, 'name': '홍길동', 'gender': '남자', 'age': '18'}]

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}: 잘못 입력된 키값

        History:
            2020-20-20(홍길동): 초기 생성
            2020-20-21(홍길동): 1차 수정
            2020-20-22(홍길동): 2차 수정
        """

        try:
            user_id = data['user_id']
            return self.cart_item_dao.get_dao(connection, user_id)

        except KeyError:
            raise KeyError('key_error')

    def post_cart_item_service(self, connection, data):
        """POST 메소드: 장바구니 상생성

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 홍길동

        Returns:
            return (): 빈값 반환

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}             : 잘못 입력된 키값
            400, {'message': 'user already exist', 'errorMessage': 'already_exist'}: 중복 유저 존재

        History:
            2020-12-28(고수희): 초기 생성
        """

        try:

            if username:
                raise UserAlreadyExist('already_exist')

            return self.cart_item_dao.post_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')
