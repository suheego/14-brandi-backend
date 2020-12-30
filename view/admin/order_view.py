from flask import jsonify
from flask.views import MethodView

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, GenderRule, AlphabeticRule

from flask_request_validator import (
    Param,
    JSON,
    validate_params,
    GET
)

class OrderListView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('order_item_status_type_id', GET, str),
        Param('order_number', GET, str, required=False),
        Param('order_detail_number', GET, str, required=False),
        Param('sender_name', GET, str, required=False),
        Param('sender_phone', GET, str, required=False),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('start_date', GET, str, required=False),
        Param('end_date', GET, str, required=False),
        Param('seller_attribute_type_ids', GET, list, required=False),
        Param('g', GET, str, required=False),
        Param('order_by', GET, str, required=False),
        Param('offset', GET, str, required=False),
        Param('limit', GET, str, required=False)
    )

    def get(self, *args):
        data = {
            'order_item_status_type_id': args[0],
            'order_number'             : args[1],
            'order_detail_number'      : args[2],
            'sender_name'              : args[3],
            'sender_phone'             : args[4],
            'seller_name'              : args[5],
            'product_name'             : args[6],
            'start_date'               : args[7],
            'end_date'                 : args[8],
            'seller_attribute_type_ids': args[9],
            'g'                        : args[10],
            'order_by'                 : args[11],
            'offset'                   : args[12],
            'limit'                    : args[13]
        }

        """GET 메소드: 해당 유저의 정보를 조회.

        user_id 에 해당되는 유저를 테이블에서 조회 후 가져온다.

        Args: args = ('user_id, )

        Author: 홍길동

        Returns:
            return {"message": "success", "result": [{"age": "18", "gender": "남자", "id": 12, "name": "홍길동"}]}

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'user does not exist error', 'errorMessage': 'user_does_not_exist'}    : 유저 정보 조회 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-20-20(홍길동): 초기 생성
            2020-20-21(홍길동): 1차 수정
            2020-20-22(홍길동): 2차 수정
        """

        try:
            connection = get_connection(self.database)
            contexts = self.service.get_prepare_product_service(connection, data)
            result = []

            for context in contexts:
                context["option_extra_cost"] = str(context["option_extra_cost"])
                context["total_price"] = str(context["total_price"])
                result.append(context)

            return jsonify({'message': 'success', 'result': result})
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('order_status_id', JSON, int)
    )
    def patch(self, *args):
        order_status_id = args[0]

        try:
            connection = get_connection(self.database)
            self.service.get_order_status_service(connection, order_status_id)
            return jsonify({'message': 'success'})
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
