from model import EventListDao


class EventListService:
    """ Business Layer

        Attributes:
            event_list_dao : EventListDao 클래스

        Author: 김민구

        History:
            2020-01-01(김민구): 초기 생성
    """

    def __init__(self):
        self.event_list_dao = EventListDao()

    def event_banner_list_logic(self, connection, data):
        """ 이벤트 배너 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : view에서 넘겨 받은 dict (offset, limit, is_proceeding)

            Author: 김민구

            Returns: 해당 기획전 배너 30개 반환
                [
                    {
                        "banner_image": "url"
                        "event_id": 1,
                        "event_kind_id": 1,
                        "event_type_id": 1
                    }
                ]

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

            History:
                2021-01-01(김민구): 초기 생성
        """

        event_list = self.event_list_dao.get_event_banner_list(connection, data)
        return event_list

    def event_detail_information_logic(self, connection, event_id):
        """ 이벤트 정보 조회

            Args:
                connection : 데이터베이스 연결 객체
                event_id   : view에서 넘겨 받은 int

            Author: 김민구

            Returns: 해당 기획전 정보 반환
                {
                    "detail_image": "url"
                    "event_id": 1,
                    "event_kind_id": 1,
                    "event_kind_name": "상품",
                    "event_type_id": 1,
                    "event_type_name": "상품(이미지)",
                    "is_button": 0
                }

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

            History:
                2021-01-01(김민구): 초기 생성

            Notes:
                해당 기획전의 정보를 반환
                is_button으로 버튼 유무를 판별
        """

        event_info = self.event_list_dao.get_event_information(connection, event_id)
        return event_info

    def event_detail_button_list_logic(self, connection, event_id):
        """ 이벤트 버튼 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                event_id   : view에서 넘겨 받은 int

            Author: 김민구

            Returns: 해당 기획전의 버튼 리스트를 반환
                [
                    {
                        "event_id": 2,
                        "id": 1,
                        "name": "1번 버튼",
                        "order_index": 1
                    }
                ]

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

            History:
                2021-01-01(김민구): 초기 생성

            Notes:
                해당 기획전의 버튼 리스트를 반환
        """

        event_button_list = self.event_list_dao.get_event_button(connection, event_id)
        return event_button_list

    def event_detail_list_logic(self, connection, data):
        """ 이벤트 상품 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : view에서 넘겨 받은 dict

            Author: 김민구

            Returns: 30개의 상품을 반환
                [
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "image_url": "url",
                        "origin_price": 10000.0,
                        "product_id": 249,
                        "product_name": "성보의하루249",
                        "sales_count": 94,
                        "seller_name": "나는셀러2"
                    }
                ]
            Raises:
                400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

            History:
                2021-01-01(김민구): 초기 생성

            Notes:
                먼저 해당 기획전에 버튼이 있는지 조회
                해당 기획전에 버튼이 존재한다면 button_id 컬럼이 포함된 기획전 리스트
                아니라면 button_id 컬럼이 없는 기획전 리스트
        """

        is_button = self.event_list_dao.is_event_has_button(connection, data['event_id'])

        if is_button:
            event_button_products = self.event_list_dao.get_event_button_product_list(connection, data)
            return event_button_products
        else:
            event_products = self.event_list_dao.get_event_product_list(connection, data)
            return event_products
