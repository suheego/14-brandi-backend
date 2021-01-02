import traceback
from utils.custom_exceptions import CustomerPermissionDenied, CartItemCreateFail


class SellerShopService:
    """ Business Layer

        Attributes:
            seller_shop_dao: SellerShopDao 클래스

        Author: 고수희

        History:
            2021-01-01(고수희): 초기 생성
    """

    def __init__(self, seller_shop_dao):
        self.seller_shop_dao = seller_shop_dao

    def get_seller_info_service(self, connection, data):
        """ GET 메소드: 셀러 상세 페이지에 출력되는 셀러 정보

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
            2020-12-28(고수희): 초기 생성
        """
        try:
            #셀러정보 정보 조회
            return self.seller_shop_dao.get_seller_info_dao(connection, data)

        except KeyError:
            traceback.print_exc()
            raise KeyError('key_error')