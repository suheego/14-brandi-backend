class EventService:
    """ Business Layer

            Attributes:
                event_dao: EventDao 클래스

            Author: 강두연

            History:
                2020-12-28(강두연): 초기 생성
                2020-12-29(강두연): 이벤트 리스트 조회 서비스 생성
                2020-12-30(강두연): 이벤트 디테일 조회 서비스 생성
    """
    def __init__(self, event_dao):
        self.event_dao = event_dao

    def get_events_service(self, connection, data):
        """ GET 메소드: 이벤트 리스트 조회

            Args:
                connection: 데이터베이스 연결 객체
                data      : View 에서 넘겨받은 dict

            Author: 강두연

            Returns:
                {
                    "events": [
                        {
                            "created_at": "2020-12-28 16:40:41",
                            "end_date": "2021-03-01 00:00:00",
                            "event_kind": "버튼",
                            "event_name": "성보의 하루 시리즈2(버튼형)",
                            "event_number": 2,
                            "event_status": "진행중",
                            "event_type": "상품(이미지)",
                            "is_display": "노출",
                            "product_count": 59,
                            "start_date": "2020-10-19 00:00:00"
                        },
                        {
                            "created_at": "2020-12-28 16:40:41",
                            "end_date": "2021-03-01 00:00:00",
                            "event_kind": "상품",
                            "event_name": "성보의 하루 시리즈",
                            "event_number": 1,
                            "event_status": "진행중",
                            "event_type": "상품(이미지)",
                            "is_display": "노출",
                            "product_count": 40,
                            "start_date": "2020-10-19 00:00:00"
                        }
                    ],
                    "total_count": 2
                }

            Raises:
                400, {'message': 'key error',
                'errorMessage': 'key_error'} : 잘못 입력된 키값

            History:
                2020-12-28(강두연): 초기 생성
                2020-12-29(강두연): 검색 조건에 맞게 변형로직 작성
        """
        try:
            data['page'] = (data['page'] - 1) * data['length']
            if data['name']:
                data['name'] = '%' + data['name'] + '%'
            return self.event_dao.get_events_list(connection, data)

        except Exception as e:
            raise e

    def get_event_detail_service(self, connection, data):
        """ GET 메소드: 이벤트 상세정보 및 등록된 상품 조회

            Args:
                connection: 데이터베이스 연결 객체
                data      : View 에서 넘겨받은 dict

            Author: 강두연

            Returns:
                기획전 종류가 상품일 때
                return {
                    "event_detail": {
                        "banner_image": "https://images.unsplash.com/sample",
                        "detail_image": "https://images.unsplash.com/sample",
                        "end_date": "2021-03-01 00:00:00",
                        "event_id": 1,
                        "event_kind": "상품",
                        "event_kind_id": 1,
                        "event_name": "성보의 하루 시리즈",
                        "event_type": "상품(이미지)",
                        "event_type_id": 1,
                        "is_display": 1,
                        "start_date": "2020-10-19 00:00:00"
                    },
                    "event_products": {
                        "products": [
                            {
                                "discount_rate": 0.1,
                                "discounted_price": 9000.0,
                                "event_button_id": null,
                                "event_id": 1,
                                "id_discount": "할인",
                                "is_display": "진열",
                                "is_sale": "판매",
                                "original_price": 10000.0,
                                "product_created_at": "2020-12-25 00:17:36",
                                "product_id": 40,
                                "product_name": "성보의하루40",
                                "product_number": "P0000000000000000040",
                                "seller_name": "나는셀러6",
                                "thumbnail_image_url": "https://img.freepik.com/sample"
                            },
                            {
                                "discount_rate": 0.1,
                                "discounted_price": 9000.0,
                                "event_button_id": null,
                                "event_id": 1,
                                "id_discount": "할인",
                                "is_display": "진열",
                                "is_sale": "판매",
                                "original_price": 10000.0,
                                "product_created_at": "2020-12-25 00:17:36",
                                "product_id": 39,
                                "product_name": "성보의하루39",
                                "product_number": "P0000000000000000039",
                                "seller_name": "나는셀러9",
                                "thumbnail_image_url": "https://img.freepik.com/sample"
                            }
                        ],
                        "total_count": 2
                    }
                }
                기획전 종류가 버튼일 때
                return {
                    "event_detail": {
                        "banner_image": "https://images.unsplash.com/sample",
                        "detail_image": "https://images.unsplash.com/sample",
                        "end_date": "2021-03-01 00:00:00",
                        "event_id": 2,
                        "event_kind": "버튼",
                        "event_kind_id": 2,
                        "event_name": "성보의 하루 시리즈2(버튼형)",
                        "event_type": "상품(이미지)",
                        "event_type_id": 1,
                        "is_display": 1,
                        "start_date": "2020-10-19 00:00:00"
                    },
                    "event_buttons": [
                        {
                            "id": 1,
                            "name": "1번 버튼",
                            "order_index": 1,
                            "product_count": 20,
                            "products": [{...}]
                        },
                        {
                            "id": 2,
                            "name": "2번 버튼",
                            "order_index": 2,
                            "product_count": 18,
                            "products": [{...}]
                        }
                    ]
                }

            Raises:
                400, {'message': 'key error',
                'errorMessage': 'key_error'} : 잘못 입력된 키값

            History:
                2020-12-30(강두연): 작성
        """
        try:
            event = self.event_dao.get_event_detail(connection, data)
            event_products = self.event_dao.get_event_products(connection, data)

            result = {
                'event_detail': event
            }

            if event['event_kind_id'] == 2:
                buttons = self.event_dao.get_event_buttons(connection, data)
                for button in buttons:
                    button['products'] = [product for product in event_products if
                                          product['event_button_id'] == button['id']]
                result['event_buttons'] = buttons

            elif event['event_kind_id'] == 1:
                count = self.event_dao.get_event_products_count(connection, data)
                result['event_products'] = {
                    'products': event_products,
                    'total_count': count
                }

            return result

        except Exception as e:
            raise e
