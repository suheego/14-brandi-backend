from flask import jsonify, g
from flask.views import MethodView

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import NumberRule, GenderRule, AlphabeticRule, OrderStatusRule

from flask_request_validator import (
    Param,
    JSON,
    validate_params,
    GET
)


class OrderView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('status', GET, int, required=True, rules=[OrderStatusRule()]),
        Param('number', GET, str, required=False),
        Param('detail_number', GET, str, required=False),
        Param('sender_name', GET, str, required=False),
        Param('sender_phone', GET, str, required=False),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('start_date', GET, str, required=False),
        Param('end_date', GET, str, required=False),
        Param('seller_attributes', JSON, list, required=False),
        Param('order_by', GET, str, required=True),
        Param('page', GET, int, required=True),
        Param('length', GET, int, required=True)
    )
    def get(self, *args):
        data = {
            'permission': g.permission_id,
            'account': g.acount_id,
            'status': args[0],
            'number': args[1],
            'detail_number': args[2],
            'sender_name': args[3],
            'sender_phone': args[4],
            'seller_name': args[5],
            'product_name': args[6],
            'start_date': args[7],
            'end_date': args[8],
            'seller_attributes': args[9],
            'order_by': args[10],
            'page': args[11],
            'length': args[12]
        }

        """GET 메소드: 주문 정보 조회

        Args: 
            args = ('status', 'number', 'detail_number', 'sender_name', 'sender_phone', 'seller_name', 
                'product_name', 'start_date', 'end_date', 'seller_attributes', 'order_by', 'page', 'length')

        Author: 김민서

        Returns:
            return {
                    "message": "success", 
                    "totalCount": 2,
                    "results": [{
                        "id": 1,
                        "created_at_date": 2020-12-30 10:05:19,
                        "updated_at_date": 2020-12-30 10:05:19,
                        "order_number": 20201225000000001,
                        "order_detail_number": oidt00002,
                        "seller_name": 나는셀러8,
                        "product_name": 성보의하루2,
                        "option_information": "Black/L",
                        "option_extra_cost": 0
                        "quantity": 1
                        "customer_name": user1,  
                        "customer_phone": 01099990102, 
                        "total_price": 18000, 
                        "status": 상품준비
                    }, {
                        "id": 2,
                        "created_at_date": 2020-12-30 10:05:19,
                        "updated_at_date": 2020-12-30 10:05:19,
                        "order_number": 20201225000000001,
                        "order_detail_number": oidt00002,
                        "seller_name": 나는셀러2,
                        "product_name": 성보의하루1,
                        "option_information": "Black/S",
                        "option_extra_cost": 0,
                        "quantity": 8,
                        "customer_name": user4,
                        "customer_phone": 01099990102, 
                        "total_price": 18000, 
                        "status": 상품준비
                    }]
                }

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'must be date inputs or filter inputs', 'errorMessage': 'must_be_date_inputs_or_filter_inputs'}: 필수 파라미터 값
            403, {'message': 'no permission to get order list', 'errorMessage': 'no_permission_to_get_order_list'} : 주문 리스트 조회 권한 없음
            404, {'message': 'order does not exist', 'errorMessage': 'order_does_not_exist'} : 주문 리스트 없음
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-29(김민서): 초기 생성
            2020-12-30(김민서): 1차 수정
            2020-12-31(김민서): 2차 수정
        """

        try:
            connection = get_connection(self.database)
            contexts = self.service.get_orders_service(connection, data)
            result = []

            for context in contexts:
                context["option_extra_cost"] = str(context["option_extra_cost"])
                context["total_price"] = str(context["total_price"])
                result.append(context)
            return jsonify({'message': 'success', 'totalCount': contexts['total_count'], 'results': result})

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
