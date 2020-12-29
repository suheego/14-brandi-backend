from flask import jsonify, request
from flask.views import MethodView
from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail, DateMissingOne, EventSearchTwoInput

from utils.rules import NumberRule, EventStatusRule, EventExposureRule, DateRule
from flask_request_validator import (
    Param,
    JSON,
    GET,
    validate_params
)


class EventView(MethodView):
    """ Presentation Layer

        Attributes:
            database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
            service : EventService 클래스

        Author: 강두연

        History:
            2020-12-28(강두연): 초기 생성
            2020-12-29(강두연): 예외 처리 및 검색조건 받기 추가
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('name', GET, str, required=False),
        Param('number', GET, str, required=False, rules=[NumberRule()]),
        Param('status', GET, str, required=False, rules=[EventStatusRule()]),
        Param('exposure', GET, int, required=False, rules=[EventExposureRule()]),
        Param('page', GET, int, required=True),
        Param('length', GET, int, required=True),
        Param('start_date', JSON, str, required=False, rules=[DateRule()]),
        Param('end_date', JSON, str, required=False, rules=[DateRule()])
    )
    def get(self, *args):
        """ GET 메소드: 검색 조건에 맞는 기획전 정보를 조회.

            [이름 또는 번호], [기획전 진행상태], [노출여부], [등록일], [페이지 및 갯수] 에 알맞는 기획전을 조회한다

            Args: args = ('name', 'number', 'status', 'exposure', 'page', 'length', 'start_date', 'end_date')

            Author: 강두연

            Returns:
                return {
                    "message": "success",
                    "result": [
                        {
                            "created_at": "Mon, 28 Dec 2020 16:40:41 GMT",
                            "end_date": "Mon, 01 Mar 2021 00:00:00 GMT",
                            "event_kind": "버튼",
                            "event_name": "성보의 하루 시리즈2(버튼형)",
                            "event_number": 2,
                            "event_status": "진행중",
                            "event_type": "상품(이미지)",
                            "is_display": "노출",
                            "product_count": 59,
                            "start_date": "Mon, 19 Oct 2020 00:00:00 GMT"
                        },
                        {
                            "created_at": "Mon, 28 Dec 2020 16:40:41 GMT",
                            "end_date": "Mon, 01 Mar 2021 00:00:00 GMT",
                            "event_kind": "상품",
                            "event_name": "성보의 하루 시리즈",
                            "event_number": 1,
                            "event_status": "진행중",
                            "event_type": "상품(이미지)",
                            "is_display": "노출",
                            "product_count": 40,
                            "start_date": "Mon, 19 Oct 2020 00:00:00 GMT"
                        }
                    ]
                }

            Raises:
                400, {'message': 'key error', 'errorMessage': 'key_error'}
                400, {
                        'message': 'date inputs should be start_date and end_date',
                        'errorMessage': 'start_date or end_date is missing'
                    }
                400, {
                        'message' : 'event search inputs must be only one',
                        'errorMessage': 'search value accept only one of name or number'
                    }
                400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}
                500, {'message': 'internal server error', 'errorMessage': format(e)})

            History:
                2020-12-28(강두연): 초기 생성
                2020-12-29(강두연): 1차 수정
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
            raise EventSearchTwoInput('search value accept only one of name or number')

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
