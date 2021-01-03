import json
from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import (
    DatabaseCloseFail,
    DateMissingOne,
    SearchTwoInput,
    FilterDoesNotMatch,
    SearchFilterRequired,
    EventKindDoesNotMatch,
    ButtonsMinimumCount,
    StartAndEndDateContext,
    ImageIsRequired,
    ProductButtonNameRequired
)

from utils.rules import (
    NumberRule,
    EventStatusRule,
    BooleanRule,
    DateRule,
    ProductMenuRule,
    CategoryFilterRule,
    PageRule,
    DateTimeRule,
)

from flask_request_validator import (
    Param,
    PATH,
    JSON,
    FORM,
    GET,
    validate_params
)


class EventView(MethodView):
    """ Presentation Layer

        Attributes:
            self.service  : EventService 클래스
            self.database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 강두연

        History:
            2020-12-28(강두연): 초기 생성, 기획전 조회 기능 작성
            2020-12-29(강두연): 기획전 조회 검색 필터링 기능 작성
            2021-01-02(강두연): 기획전 생성기능 작성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('name', GET, str, required=False),
        Param('number', GET, str, required=False, rules=[NumberRule()]),
        Param('status', GET, str, required=False, rules=[EventStatusRule()]),
        Param('exposure', GET, int, required=False, rules=[BooleanRule()]),
        Param('page', GET, int, required=True, rules=[PageRule()]),
        Param('length', GET, int, required=True),
        Param('start_date', JSON, str, required=False, rules=[DateRule()]),
        Param('end_date', JSON, str, required=False, rules=[DateRule()])
    )
    def get(self, *args):
        """ GET 메소드: 이벤트 리스트 조회

            Args:
                args[0](name): 기획전 이름
                args[1](number): 기획전 번호
                args[2](status): 기획전 상태
                args[3](exposure): 노출 여부
                args[4](page): 페이지 번호
                args[5](length): 페이지네이션 리미트
                args[6](start_date): 등록일 기준 검색할 때 시작날짜
                args[7](end_date): 등록일 기준 검색할 때 끝나는날짜

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
                400, {'message': 'search inputs must be only one',
                'errorMessage': 'search value accept only one of name or number'} : 동시에 사용할수 없는 필터가 들어왔을 때

                400, {'message': 'date inputs should be start_date and end_date',
                'errorMessage': 'start_date or end_date is missing'} : 등록일로 검색할 때 시작일 또는 종료일이 하나만 있는경우

            History:
                2020-12-28(강두연): 초기 생성
                2020-12-29(강두연): 검색 조건에 맞게 필터링 기능 작성
        """

        data = {
            'name': args[0],
            'number': args[1],
            'status': args[2],
            'exposure': args[3],
            'page': args[4],
            'length': args[5],
            'start_date': args[6],
            'end_date': args[7]
        }
        if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
            raise DateMissingOne('start_date or end_date is missing')

        if data['name'] and data['number']:
            raise SearchTwoInput('search value accept only one of name or number')

        try:
            connection = get_connection(self.database)
            events = self.service.get_events_service(connection, data)
            return jsonify({'message': 'success', 'result': events})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('name', FORM, str, required=True),
        Param('start_datetime', FORM, str, required=True, rules=[DateTimeRule()]),
        Param('end_datetime', FORM, str, required=True, rules=[DateTimeRule()]),
        Param('event_type_id', FORM, int, required=True),
        Param('event_kind_id', FORM, int, required=True),
        Param('is_display', FORM, int, required=True, rules=[BooleanRule()]),
        Param('buttons', FORM, list, required=False),
        Param('products', FORM, list, required=False)
    )
    def post(self, *args):
        """ 기획전 등록

            Args:
                name: 기획전 이름
                start_datetime: 기획전 시작날짜시간
                end_datetime: 기획전 종료날짜시간
                event_type_id: 기획전 타입
                event_kind_id: 기획전 종류
                is_display: 노출여부
                buttons: 기획전에 추가할 버튼
                products: 기획전에 추가할 상품
                banner_image: 배너이미지 파일
                detail_image: 상세이미지 파일

            Returns:
                생성된 기획전 아이디

            Raises:
                400, {'message': 'at least two buttons should be created',
                      'errorMessage': 'button is required'} : 기획전 종류가 버튼형일때 버튼이 없을 때

                400, {'message': 'at least two buttons should be created',
                      'errorMessage': 'at least two buttons are required'} : 기획전 종류가 버튼인데 2개 미만의 버튼이 들어왔을 때

                400, {
                    'message': 'button name is required in each product',
                    'errorMessage': 'button name is required in each product'
                } : 기획전 종류가 버튼인데 상품에 버튼이름 키,값이 없을 때

                400, {'message': 'Event kind does not match',
                      'errorMessage': 'event kind is not buttons'} : 기획전 종류가 버튼형이 아닌데 버튼들에 대한 정보가 들어왔을 때

                400, {'message': 'image files are required',
                      'errorMessage': 'image is required'} : 이미지가 필요함

                400, {'message': 'start date and end date context error',
                      'errorMessage': 'start and end datetime context error'} : 시작날짜가 종료날짜보다 미래일 때

            History:
                    2020-01-02(강두연): 초기 작성
        """
        data = {
            'name': request.form.get('name'),
            'start_datetime': request.form.get('start_datetime'),
            'end_datetime': request.form.get('end_datetime'),
            'event_type_id': request.form.get('event_type_id'),
            'event_kind_id': request.form.get('event_kind_id'),
            'is_display': request.form.get('is_display')
        }

        banner_image = request.files.get('banner_image')
        detail_image = request.files.get('detail_image')

        buttons = request.form.get('buttons')
        products = request.form.get('products')

        if products:
            products = json.loads(products)

        if data['event_kind_id'] == '2':
            # 기획전 종류가 버튼인데 버튼이 없을 때
            if not buttons:
                raise ButtonsMinimumCount('button is required')

            buttons = json.loads(buttons)

            # 기획전 종류가 버튼인데 2개 미만의 버튼이 들어왔을 때
            if len(buttons) < 2:
                raise ButtonsMinimumCount('at least two buttons are required')

            # 기획전 종류가 버튼인데 상품에 버튼이름 키,값이 없을 때
            if products:
                for product in products:
                    if 'button_name' not in product or not product['button_name']:
                        raise ProductButtonNameRequired('button name is required in each product')

        # 기획전 종류가 버튼형이 아닌데 버튼들에 대한 정보가 들어왔을 때
        elif data['event_kind_id'] != '2' and buttons:
            raise EventKindDoesNotMatch('event kind is not buttons')

        # 이미지 파일 존재 유무 확인
        if not banner_image or not detail_image or not banner_image.filename or not detail_image.filename:
            raise ImageIsRequired('image is required')

        data['banner_image'] = banner_image
        data['detail_image'] = detail_image

        # 시작 날짜가 종료날짜보다 미래일 때
        start = datetime.strptime(data['start_datetime'], "%Y-%m-%d %H:%M")
        end = datetime.strptime(data['end_datetime'], "%Y-%m-%d %H:%M")

        if start >= end:
            raise StartAndEndDateContext('start and end datetime context error')

        try:
            connection = get_connection(self.database)
            result = self.service.create_event_service(connection, data, buttons, products)

            connection.commit()

            return jsonify({'message': 'success', 'event_id': result}), 201

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class EventDetailView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : EventService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 강두연

        History:
            2020-12-31(강두연): 초기 생성, 기획전 상세정보 조회 기능 작성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('event_id', PATH, int, required=True)
    )
    def get(self, *args):
        """ 이벤트 상세정보 및 등록된 상품 조회

            Args:
               args[0](event_id) : 이벤트 아이디

            Author: 강두연

            Returns:
                기획전 종류가 상품일 때
                {
                    "message": "success",
                    "result": {
                        "event_detail": {
                            "banner_image": "https://brandi-intern-8.s3.amazonaws.com/events/2021/01/03/banners",
                            "detail_image": "https://brandi-intern-8.s3.amazonaws.com/events/2021/01/03/details",
                            "end_date": "2021-01-05 23:13:00",
                            "event_id": 20,
                            "event_kind": "상품",
                            "event_kind_id": 1,
                            "event_name": "이벤트(상품동시추가)생성",
                            "event_type": "상품(이미지)",
                            "event_type_id": 1,
                            "is_display": 1,
                            "start_date": "2021-01-02 12:13:00"
                        },
                        "event_products": {
                            "products": [
                                {
                                    "discount_rate": 0.1,
                                    "discounted_price": 9000.0,
                                    "event_button_id": null,
                                    "event_id": 20,
                                    "id_discount": "할인",
                                    "is_display": "진열",
                                    "is_sale": "판매",
                                    "original_price": 10000.0,
                                    "product_created_at": "2020-12-25 00:17:36",
                                    "product_id": 3,
                                    "product_name": "성보의하루3",
                                    "product_number": "P0000000000000000003",
                                    "seller_name": "나는셀러2",
                                    "thumbnail_image_url": "https://img.freepik.com/free-psd"
                                },
                                {
                                    "discount_rate": 0.1,
                                    "discounted_price": 9000.0,
                                    "event_button_id": null,
                                    "event_id": 20,
                                    "id_discount": "할인",
                                    "is_display": "진열",
                                    "is_sale": "판매",
                                    "original_price": 10000.0,
                                    "product_created_at": "2020-12-25 00:17:36",
                                    "product_id": 2,
                                    "product_name": "성보의하루2",
                                    "product_number": "P0000000000000000002",
                                    "seller_name": "나는셀러8",
                                    "thumbnail_image_url": "https://img.freepik.com/free-psd"
                                }
                            ],
                            "total_count": 2
                        }
                    }
                }
                기획전 종류가 버튼일 때
                {
                    "message": "success",
                    "result": {
                        "event_buttons": [
                            {
                                "id": 4,
                                "name": "버튼1",
                                "order_index": 1,
                                "product_count": 1,
                                "products": [
                                    {
                                        "discount_rate": 0.1,
                                        "discounted_price": 9000.0,
                                        "event_button_id": 4,
                                        "event_id": 22,
                                        "id_discount": "할인",
                                        "is_display": "진열",
                                        "is_sale": "판매",
                                        "original_price": 10000.0,
                                        "product_created_at": "2020-12-25 00:17:36",
                                        "product_id": 1,
                                        "product_name": "성보의하루1",
                                        "product_number": "P0000000000000000001",
                                        "seller_name": "나는셀러9",
                                        "thumbnail_image_url": "https://img.freepik.com/free-psd"
                                    }
                                ]
                            },
                            {
                                "id": 5,
                                "name": "버튼2",
                                "order_index": 2,
                                "product_count": 2,
                                "products": [
                                    {
                                        "discount_rate": 0.1,
                                        "discounted_price": 9000.0,
                                        "event_button_id": 5,
                                        "event_id": 22,
                                        "id_discount": "할인",
                                        "is_display": "진열",
                                        "is_sale": "판매",
                                        "original_price": 10000.0,
                                        "product_created_at": "2020-12-25 00:17:36",
                                        "product_id": 3,
                                        "product_name": "성보의하루3",
                                        "product_number": "P0000000000000000003",
                                        "seller_name": "나는셀러2",
                                        "thumbnail_image_url": "https://img.freepik.com/free-psd"
                                    },
                                    {
                                        "discount_rate": 0.1,
                                        "discounted_price": 9000.0,
                                        "event_button_id": 5,
                                        "event_id": 22,
                                        "id_discount": "할인",
                                        "is_display": "진열",
                                        "is_sale": "판매",
                                        "original_price": 10000.0,
                                        "product_created_at": "2020-12-25 00:17:36",
                                        "product_id": 2,
                                        "product_name": "성보의하루2",
                                        "product_number": "P0000000000000000002",
                                        "seller_name": "나는셀러8",
                                        "thumbnail_image_url": "https://img.freepik.com/free-psd"
                                    }
                                ]
                            }
                        ],
                        "event_detail": {
                            "banner_image": "https://brandi-intern-8.s3.amazonaws.com/events/2021/01/03/banners",
                            "detail_image": "https://brandi-intern-8.s3.amazonaws.com/events/2021/01/03/details",
                            "end_date": "2021-01-05 23:13:00",
                            "event_id": 22,
                            "event_kind": "버튼",
                            "event_kind_id": 2,
                            "event_name": "이벤트(상품동시추가)생성",
                            "event_type": "상품(이미지)",
                            "event_type_id": 1,
                            "is_display": 1,
                            "start_date": "2021-01-02 12:13:00"
                        }
                    }
                }

            History:
                2020-12-31(강두연): 작성
        """
        data = {
            'event_id': args[0]
        }

        try:
            connection = get_connection(self.database)
            result = self.service.get_event_detail_service(connection, data)
            return jsonify({"message": "success", "result": result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class EventProductsCategoryView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : EventService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 강두연

        History:
            2020-12-31(강두연): 초기 생성, 기획전 상품추가 상품 카테고리 조회 기능 작성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('filter', JSON, str, required=True, rules=[CategoryFilterRule()]),
        Param('menu_id', JSON, int, required=False, rules=[ProductMenuRule()]),
        Param('first_category_id', JSON, int, required=False)
    )
    def get(self, *args):
        """ 기획전에 상품추가 페이지에서 상품 카테고리 받아오기

            Args:
                args[0](filter): 데이터베이스 연결 객체
                args[1](menu_id): 메뉴 아이디
                args[2](first_category_id): 1차 카테고리 아이디

            Author: 강두연

            Returns:
                case1: {
                    "message": "success",
                    "result": [
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
                }

                case2: {
                    "message": "success",
                    "result": [
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
                }

                case3: {
                    "message": "success",
                    "result": [
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
                }

            Raises:
                400, {'message': 'filter does not match',
                'errorMessage': 'upper category is required'} : 키 'filter' 의 값과 주어진 필터링 데이터가 알맞지 않는경우

            History:
                2020-12-31(강두연): 초기 작성
        """

        data = {
            'filter': args[0],
            'menu_id': args[1],
            'first_category_id': args[2]
        }
        if data['filter'] == "none" and (data['menu_id'] or data['first_category_id']):
            raise FilterDoesNotMatch('error: filter does not match')
        elif data['filter'] == "menu":
            if not data['menu_id']:
                raise FilterDoesNotMatch('error: filter does not match')
            if data['first_category_id']:
                raise FilterDoesNotMatch('error: filter does not match')
        elif data['filter'] == "both":
            if not data['menu_id'] or not data['first_category_id']:
                raise FilterDoesNotMatch('error: filter does not match')

        try:
            connection = get_connection(self.database)
            result = self.service.get_products_category_service(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class EventProductsToAddView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : EventService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 강두연

        History:
            2020-12-31(강두연): 초기 생성, 기획전 상품추가 페이지 상품 조회 기능 작성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('product_name', GET, str, required=False),
        Param('product_number', GET, str, required=False, rules=[NumberRule()]),
        Param('seller_name', GET, str, required=False),
        Param('seller_number', GET, str, required=False, rules=[NumberRule()]),
        Param('menu_id', JSON, int, required=False, rules=[ProductMenuRule()]),
        Param('main_category_id', JSON, int, required=False),
        Param('sub_category_id', JSON, int, required=False),
        Param('page', GET, int, required=True, rules=[PageRule()]),
        Param('length', GET, int, required=True),
        Param('start_date', JSON, str, required=False, rules=[DateRule()]),
        Param('end_date', JSON, str, required=False, rules=[DateRule()])
    )
    def get(self, *args):
        """ 기획전에 추가할 상품 조회

            Args:
                args[0](product_name): 상품이름
                args[1](product_number): 상품번호
                args[2](seller_name): 셀러명
                args[3](seller_number): 셀러번호
                args[4](menu_id): 메뉴 아이디 - 트렌드 4, 브렌드 5, 뷰티 6
                args[5](main_category_id): 1차 카테고리 아이디
                args[6](sub_category_id): 2차 카테고리 아이디
                args[7](page): 페이지 번호
                args[8](length): 페이지네이션 리미트
                args[9](start_date): 등록일 기준 검색할 때 시작날짜
                args[10](end_date): 등록일 기준 검색할 때 끝나는날짜

            Returns: {
                "message": "success",
                "result": {
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
                            "thumbnail_image_url": "https://img.freepik.com"
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
                            "thumbnail_image_url": "https://img.freepik.com"
                        }
                    ],
                    "total_count": 31
                }
            }

            Raises:
                400, {'message': 'filter must be at least one',
                'errorMessage': 'search filter must be at least one'} : 검색 필터가 하나도 없을 때

                400, {'message': 'search inputs must be only one',
                'errorMessage': 'search value accept only one of name or number'} : 동시에 사용할수 없는 필터가 들어왔을 때

                400, {'message': 'filter does not match',
                'errorMessage': 'upper category is required'} : 상품 분류로 검색할 때 하위카테고리만 있고 상위카테고리는 없는경우

                400, {'message': 'date inputs should be start_date and end_date',
                'errorMessage': 'start_date or end_date is missing'} : 등록일로 검색할 때 시작일 또는 종료일이 하나만 있는경우

            History:
                    2020-12-31(강두연): 초기 작성
        """

        data = {
            'product_name': args[0],
            'product_number': args[1],
            'seller_name': args[2],
            'seller_number': args[3],
            'menu_id': args[4],
            'main_category_id': args[5],
            'sub_category_id': args[6],
            'page': args[7],
            'length': args[8],
            'start_date': args[9],
            'end_date': args[10]
        }
        if not data['product_name'] \
                and not data['product_number'] \
                and not data['seller_number'] \
                and not data['seller_name'] \
                and not data['menu_id'] \
                and not (data['start_date'] and data['end_date']):
            raise SearchFilterRequired('search filter must be at least one')

        if (data['product_number'] and data['product_name']) or (data['seller_number'] and data['seller_name']):
            raise SearchTwoInput('search value accept only one of name or number')

        if not data['menu_id'] and (data['main_category_id'] or data['sub_category_id']):
            raise FilterDoesNotMatch('upper category is required')

        if not data['main_category_id'] and data['sub_category_id']:
            raise FilterDoesNotMatch('upper category is required')

        if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
            raise DateMissingOne('start_date or end_date is missing')

        try:
            connection = get_connection(self.database)
            products = self.service.get_products_to_post_service(connection, data)
            return jsonify({'message': 'success', 'result': products})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
