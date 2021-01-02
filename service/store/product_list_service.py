from model import ProductListDao


class ProductListService:
    """ Business Layer

        Attributes:
            product_dao : ProductListDao 클래스

        Author: 김민구

        History:
            2020-12-30(김민구): 초기 생성
            2020-12-31(김민구): 수정 (product_dao를 import 해서 사용하는 방법으로 수정)
    """

    def __init__(self):
        self.product_dao = ProductListDao()

    def product_list_logic(self, connection, offset):
        """ 상품 리스트와 이벤트 배너 조회

            Args:
                connection : 데이터베이스 연결 객체
                offset     : View 에서 넘겨받은 int

            Author: 김민구

            Returns: 해당 이벤트 배너와 30개의 상품을 반환

                    "event": {
                        'id' : 1,
                        'banner_image' : 'url'
                    },
                    "product_list" : [
                        {
                            'image': 'url',
                            'seller_id': 1,
                            'seller_name': '둘리',
                            'product_id': 1,
                            'product_name': '성보의 하루',
                            'origin_price': 10000.0,
                            'discount_rate': 0.1,
                            'discounted_price': 9000.0,
                            'sales_count': 30
                        },
                ]

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경 / 이벤트에 해당하는 상품리스트를 반환하는 작업으로 수정
        """

        event = self.product_dao.get_event(connection, offset)
        if not event:
            return []
        product_list = self.product_dao.get_product_list(connection, event['event_id'])
        return {'event': event, 'product_list': product_list}
    
    def product_search_service(self, connection, search):
        """ 상품 검색 서비스

            1. 입력받은 값과 같은 상품이 존재한지 알아본다.

            Args:
                connection: 데이터베이스 연결 객체
                search    : 쿼리스트링이 담긴 변수

            Author: 김기용

            Returns: ###

            Raises: ###

            History:
                2020-12-31(김기용): 초기 생성

        """
        return self.product_dao.get_search_products_dao(connection, search)

