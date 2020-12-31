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

            Returns:
                [{product_info},{event_info}]

            Raises:
                400, {'message': 'key_error', 'errorMessage': format(e)} : 잘못 입력된 키값

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 수정
        """

        event = self.product_dao.get_event(connection, offset)
        if not event:
            return []
        product_list = self.product_dao.get_product_list(connection, event['event_id'])
        return [event] + product_list

