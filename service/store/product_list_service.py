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
    
    def product_search_service(self, connection, data):
        """ 상품 검색 서비스

            Args:
                connection: 데이터베이스 연결 객체
                search    : 쿼리스트링이 담긴 변수

            Author: 김기용

            Returns: {
                        "bookmark_count": 0,
                        "discounted_price": 9000.0,
                        "image": "https://img.freepik.com",
                        "name": "성보의하루999",
                        "origin_price": 10000.0,
                        "product_id": 999,
                        "sales_count": 32,
                        "seller_id": 4,
                        "seller_name": "나는셀러4"
                        }
            Raises: None

            History:
                2020-12-31(김기용): 초기 생성

        """
        return self.product_dao.get_search_products_dao(connection, data)
    
    def product_detail_service(self, connection, data):
        """ 상품상세정보 조회 서비스

            Args:
                connection: 데이터베이스 연결 객체
                search    : 쿼리스트링이 담긴 변수

            Author: 김기용

            Returns: 상제 제품 정보
            Raises: 

            History:
                2020-12-31(김기용): 초기 생성
                2020-01-05(김기용): 누락된여러개의 size와 color 값을 추가
        """

        # product_image를 가져온다
        images = self.product_dao.get_product_image_dao(connection, data)
        sizes = self.product_dao.get_product_size_dao(connection, data)
        colors = self.product_dao.get_product_color_dao(connection, data)
        product = self.product_dao.get_product_detail_dao(connection, data)
        product['colors'] = colors
        product['sizes'] = sizes
        product['images'] = images 

        return product
        
