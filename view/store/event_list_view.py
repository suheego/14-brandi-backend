from flask.views import MethodView
from flask import jsonify

from flask_request_validator import (
    validate_params,
    Param,
    GET,
    PATH
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import PositiveInteger


class EventBannerListView(MethodView):
    """ Presentation Layer

        Attributes:
            event_list_service : EventListService 클래스
            database           : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-01-01(김민구): 초기 생성
    """

    def __init__(self, services, database):
        self.event_list_service = services.event_list_service
        self.database = database

    @validate_params(
        Param('offset', GET, int),
        Param('is_proceeding', GET, bool)
    )
    def get(self, *args):
        """ GET 메소드: 기획전 배너 리스트 조회

            Args:
                offset = 0부터 시작
                is_proceeding = 0 or 1

            Author: 김민구

            Returns: 기획전 배너 리스트 조회 성공
                200, {
                        'message': 'success',
                        'result': [
                            {
                                "banner_image": "url"
                                "event_id": 1,
                                "event_kind_id": 1,
                                "event_type_id": 1
                            }
                        ]
                    }

            Raises:
                400, {'message': 'invalid_parameter', 'error_message': '[데이터]가(이) 유효하지 않습니다.'}  : 잘못된 요청값
                400, {'message': 'key_error', 'error_message': format(e)}                            : 잘못 입력된 키값
                500, {
                    'message': 'database_connection_fail',
                    'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                    }                                                                                : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러

            History:
                2020-01-01(김민구): 초기 생성

            Notes:
                is_proceeding이 0이면 종료된 기획전 배너 리스트르 반환, 1이면 진행중인 기획전 배너 리스트를 반환
        """

        connection = None
        try:
            data = {
                'offset': args[0],
                'is_proceeding': args[1]
            }
            connection = get_connection(self.database)
            result = self.event_list_service.event_banner_list_logic(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class EventDetailInformationView(MethodView):
    """ Presentation Layer

        Attributes:
            event_list_service : EventListService 클래스
            database           : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-01-01(김민구): 초기 생성
    """

    def __init__(self, services, database):
        self.event_list_service = services.event_list_service
        self.database = database

    @validate_params(
        Param('event_id', PATH, int, rules=[PositiveInteger()])
    )
    def get(self, *args):
        """ GET 메소드: 기획전 정보 조회

            Args:
                event_id = 기획전 아이디

            Author: 김민구

            Returns: 기획전 정보 조회 성공
                200, {
                        'message': 'success',
                        'result': {
                            "detail_image": "url"
                            "event_id": 1,
                            "event_kind_id": 1,
                            "event_kind_name": "상품",
                            "event_type_id": 1,
                            "event_type_name": "상품(이미지)",
                            "is_button": 0
                        }
                    }

            Raises:
                400, {'message': 'invalid_parameter', 'error_message': '[데이터]가(이) 유효하지 않습니다.'}  : 잘못된 요청값
                400, {'message': 'key_error', 'error_message': format(e)}                            : 잘못 입력된 키값
                500, {
                    'message': 'database_connection_fail',
                    'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                    }                                                                                : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러

            History:
                2020-01-01(김민구): 초기 생성
        """

        connection = None
        try:
            event_id = args[0]
            connection = get_connection(self.database)
            result = self.event_list_service.event_detail_information_logic(connection, event_id)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class EventDetailButtonListView(MethodView):
    """ Presentation Layer

        Attributes:
            event_list_service : EventListService 클래스
            database           : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-01-01(김민구): 초기 생성
    """

    def __init__(self, services, database):
        self.event_list_service = services.event_list_service
        self.database = database

    @validate_params(
        Param('event_id', PATH, int, rules=[PositiveInteger()])
    )
    def get(self, *args):
        """ GET 메소드: 기획전 버튼 리스트 조회

            Args:
                event_id = 기획전 아이디

            Author: 김민구

            Returns: 기획전 버튼 리스트 조회 성공
                200, {
                        'message': 'success',
                        'result': [
                            {
                                "event_id": 2,
                                "id": 1,
                                "name": "1번 버튼",
                                "order_index": 1
                            }
                        ]
                    }

            Raises:
                400, {'message': 'invalid_parameter', 'error_message': '[데이터]가(이) 유효하지 않습니다.'}  : 잘못된 요청값
                400, {'message': 'key_error', 'error_message': format(e)}                            : 잘못 입력된 키값
                500, {
                    'message': 'database_connection_fail',
                    'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                    }                                                                                : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러

            History:
                2020-01-01(김민구): 초기 생성
        """

        connection = None
        try:
            event_id = args[0]
            connection = get_connection(self.database)
            result = self.event_list_service.event_detail_button_list_logic(connection, event_id)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')


class EventDetailProductListView(MethodView):
    """ Presentation Layer

        Attributes:
            event_list_service : EventListService 클래스
            database           : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 김민구

        History:
            2020-01-01(김민구): 초기 생성
    """

    def __init__(self, services, database):
        self.event_list_service = services.event_list_service
        self.database = database

    @validate_params(
        Param('offset', GET, int),
        Param('event_id', PATH, int, rules=[PositiveInteger()])
    )
    def get(self, *args):
        """ GET 메소드: 기획전 상품 리스트 조회

            Args:
                offset = 0부터 시작 (30 단위)
                event_id = 기획전 아이디

            Author: 김민구

            Returns: 기획전 상품 리스트 조회 성공
                200, {
                        'message': 'success',
                        'result': [
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
                    }

            Raises:
                400, {'message': 'invalid_parameter', 'error_message': '[데이터]가(이) 유효하지 않습니다.'}  : 잘못된 요청값
                400, {'message': 'key_error', 'error_message': format(e)}                            : 잘못 입력된 키값
                500, {
                    'message': 'database_connection_fail',
                    'error_message': '서버에 알 수 없는 에러가 발생했습니다.'
                    }                                                                                : 커넥션 종료 실패
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'}  : 데이터베이스 에러
                500, {'message': 'internal_server_error', 'error_message': format(e)})               : 서버 에러

            History:
                2020-01-01(김민구): 초기 생성

            Notes:
                해당 기획전에 버튼이 존재한다면 button_id 컬럼이 포함된 기획전 리스트
                아니라면 button_id 컬럼이 없는 기획전 리스트
        """

        connection = None
        try:
            data = {
                'offset': args[0],
                'event_id': args[1]
            }
            connection = get_connection(self.database)
            result = self.event_list_service.event_detail_list_logic(connection, data)
            return jsonify({'message': 'success', 'result': result})

        except Exception as e:
            raise e

        finally:
            try:
                if connection is not None:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('서버에 알 수 없는 에러가 발생했습니다.')