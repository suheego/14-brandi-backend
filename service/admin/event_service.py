import datetime

from werkzeug.utils import secure_filename
from utils.custom_exceptions import ButtonProductDoesNotMatch, EventDoesNotExist
from utils.amazon_s3 import S3FileManager, GenerateFilePath

from config import S3_BUCKET_URL


class EventService:
    """ Business Layer

            Attributes:
                event_dao: EventDao 클래스

            Author: 강두연

            History:
                2020-12-28(강두연): 초기 생성
                2020-12-29(강두연): 이벤트 리스트 조회 서비스 생성
                2020-12-30(강두연): 이벤트 디테일 조회 서비스 생성
                2020-12-31(강두연): 기획전 상품추가 페이지 카테고리 불러오기 서비스 생성
                2020-12-31(강두연): 기획전 상품추가 페이지 상품 리스트 불러오기 서비스 생성
                2021-01-02(강두연): 기획전 등록 서비스 생성
                2021-01-02(강두연): 기획전 삭제 서비스 생성
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

    def get_products_category_service(self, connection, data):
        """ 기획전에 상품추가 페이지에서 상품 카테고리 받아오기

            Args:
                connection: 데이터베이스 연결 객체
                data      : View 에서 넘겨받은 dict

            Author: 강두연

            Returns:
                case 1: [
                    {
                        "id": 4,
                        "name": "트렌드"
                    },
                    {
                        "id": 5,
                        "name": "브랜드"
                    },
                    {
                        "id": 6,
                        "name": "뷰티"
                    }
                ]
                case 2: [
                    {
                        "id": 1,
                        "name": "아우터"
                    },
                    {
                        "id": 2,
                        "name": "상의"
                    },
                    {
                        "id": 3,
                        "name": "바지"
                    },
                    {
                        "id": 4,
                        "name": "원피스"
                    },
                    {
                        "id": 5,
                        "name": "스커트"
                    },
                    {
                        "id": 6,
                        "name": "신발"
                    },
                    {
                        "id": 7,
                        "name": "가방"
                    },
                    {
                        "id": 8,
                        "name": "주얼리"
                    },
                    {
                        "id": 9,
                        "name": "잡화"
                    },
                    {
                        "id": 10,
                        "name": "라이프웨어"
                    },
                    {
                        "id": 11,
                        "name": "빅사이즈"
                    }
                ]
                case 3: [
                    {
                        "id": 1,
                        "name": "자켓"
                    },
                    {
                        "id": 2,
                        "name": "가디건"
                    },
                    {
                        "id": 3,
                        "name": "코트"
                    },
                    {
                        "id": 4,
                        "name": "점퍼"
                    },
                    {
                        "id": 5,
                        "name": "패딩"
                    },
                    {
                        "id": 6,
                        "name": "무스탕/퍼"
                    },
                    {
                        "id": 7,
                        "name": "기타"
                    }
                ]

            Raises:
                400, {'message': 'key error',
                'errorMessage': 'key_error'} : 잘못 입력된 키값

            History:
                2020-12-31(강두연): 초기 작성
        """
        try:
            return self.event_dao.get_product_category(connection, data)

        except Exception as e:
            raise e

    def get_products_to_post_service(self, connection, data):
        """ 기획전에 추가할 상품 조회

            Args:
                connection: 데이터베이스 연결 객체
                data : 뷰에서 넘겨 받은 딕셔너리

            Returns: {
                "products": [
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "id": 99,
                        "is_display": 1,
                        "is_sale": 1,
                        "original_price": 10000.0,
                        "product.discounted_price": 9000.0,
                        "product_name": "성보의하루99",
                        "product_number": "P0000000000000000099",
                        "seller_name": "나는셀러5",
                        "thumbnail_image_url": "https://img.com/asdf"
                    },
                    {
                        "discount_rate": 0.1,
                        "discounted_price": 9000.0,
                        "id": 98,
                        "is_display": 1,
                        "is_sale": 1,
                        "original_price": 10000.0,
                        "product.discounted_price": 9000.0,
                        "product_name": "성보의하루98",
                        "product_number": "P0000000000000000098",
                        "seller_name": "나는셀러5",
                        "thumbnail_image_url": "https://img.com/asdf"
                    }
                ],
                "total_count": 31
            }

            Raises:
                400, {'message': 'key error',
                'errorMessage': 'key_error'} : 잘못 입력된 키값

            History:
                    2020-12-31(강두연): 초기 작성
        """

        try:
            data['page'] = (data['page']-1) * data['length']
            if data['product_name']:
                data['product_name'] = '% ' + data['product_name'] + ' %'
            return self.event_dao.get_products_list_to_post(connection, data)

        except Exception as e:
            raise e

    def create_event_service(self, connection, data, buttons=None, products=None):
        """ 기획전 등록

            Args:
                connection: 데이터베이스 연결 객체
                data: 뷰에서 넘겨 받은 딕셔너리
                buttons: 상품이 버튼형일때 버튼에 대한 정보를 담고있는 딕셔너리 리스트
                products: 기획전에 추가할 상품이 있을 때 상품에 대한 정보를 담고있는 딕셔너리 리스트

            Returns:
                생성된 기획전 아이디

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error'} : 잘못 입력된 키값

                400, {
                    'message': 'although there are product and button objects, no buttons are matched',
                    'errorMessage': ''there are product and button objects but no buttons are matched'
                } : 기획전 종류가 버튼형이고 추가할 상 객체가 있지만 상품과 매치된 버튼이 단 하나도 없음

            History:
                    2020-01-02(강두연): 초기 작성
        """
        try:
            banner_file_path = GenerateFilePath().generate_file_path(
                4,
                today=datetime.date.today().isoformat().replace('-', '/')
            )

            secured_banner_file_name = secure_filename(data['banner_image'].filename)

            detail_file_path = GenerateFilePath().generate_file_path(
                5,
                today=datetime.date.today().isoformat().replace('-', '/')
            )

            secured_detail_file_name = secure_filename(data['detail_image'].filename)

            # save to AMAZON S3
            data['banner_image'] = S3FileManager().file_upload(
                data['banner_image'],
                banner_file_path + secured_banner_file_name
            )

            data['detail_image'] = S3FileManager().file_upload(
                data['detail_image'],
                detail_file_path + secured_detail_file_name
            )

            data['banner_image'] = S3_BUCKET_URL + data['banner_image']
            data['detail_image'] = S3_BUCKET_URL + data['detail_image']
            data['start_datetime'] += ':00'
            data['end_datetime'] += ':00'

            data['event_id'] = self.event_dao.create_event(connection, data)

            if products and buttons:
                button_product_matched = False

            if buttons:
                for button in buttons:
                    button['event_id'] = data['event_id']
                    button_id = self.event_dao.create_button(connection, button)
                    if products:
                        for product in products:
                            if product['button_name'] == button['button_name']:
                                product['button_id'] = button_id
                                product['event_id'] = data['event_id']
                                button_product_matched = True
                                self.event_dao.insert_product_into_button(connection, product)

            if not button_product_matched:
                raise ButtonProductDoesNotMatch('there are product and button objects but no buttons are matched')

            elif not buttons and products:
                for product in products:
                    product['event_id'] = data['event_id']
                    self.event_dao.insert_product_into_event(connection, product)

            return data['event_id']

        except Exception as e:
            raise e

    def event_delete_service(self, connection, data):
        """ 기획전 삭제

            Args:
                connection: 데이터베이스 연결 객체
                data: 뷰에서 넘겨 받은 딕셔너리

            Returns:
                성공여부

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error'} : 잘못 입력된 키값

            History:
                    2020-01-04(강두연): 초기 작성
        """
        try:
            # 존재하지 않는 기획전 아이디 이거나, 논리삭제값이 0이 아닌경우 예외 처리포함
            event = self.event_dao.get_event_detail(connection, data)

            if event['event_kind_id'] == 2:
                self.event_dao.delete_buttons_by_event(connection, data)

            self.event_dao.delete_event_products_by_event(connection, data)
            self.event_dao.delete_event(connection, data)

            return True

        except Exception as e:
            raise e
