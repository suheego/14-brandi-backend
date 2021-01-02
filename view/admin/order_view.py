from flask import jsonify, g
from flask.views import MethodView

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import OrderStatusRule, DateRule

from flask_request_validator import (
    Param,
    JSON,
    validate_params,
    GET,
    PATH
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
        Param('start_date', GET, str, required=False), #rules=[DateRule()]),
        Param('end_date', GET, str, required=False), #rules=[DateRule()]),
        Param('attributes', GET, list, required=False),
        Param('order_by', GET, str, required=True),
        Param('page', GET, int, required=True),
        Param('length', GET, str, required=True)
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
            'attributes': args[9],
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
            {
                "message": "success",
                "results": [
                    {
                        "created_at_date": "2020-12-30 10:05:19",
                        "customer_name": "user2",
                        "customer_phone": "01099990103",
                        "id": 3,
                        "option_extra_cost": "0",
                        "option_information": "Black/Free",
                        "order_detail_number": "oidt00003",
                        "order_number": "20201225000000002",
                        "product_name": "성보의하루1",
                        "quantity": 1,
                        "seller_name": "나는셀러9",
                        "status": "상품준비",
                        "total_price": "9000",
                        "updated_at_date": "2020-12-30 10:05:19"
                    },
                    {
                        "created_at_date": "2020-12-30 10:05:19",
                        "customer_name": "user1",
                        "customer_phone": "01099990102",
                        "id": 4,
                        "option_extra_cost": "0",
                        "option_information": "Black/Free",
                        "order_detail_number": "oidt00004",
                        "order_number": "20201225000000003",
                        "product_name": "성보의하루1",
                        "quantity": 4,
                        "seller_name": "나는셀러9",
                        "status": "상품준비",
                        "total_price": "36000",
                        "updated_at_date": "2020-12-30 10:05:19"
                    }
                ],
                "totalCount": 2
            }

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'must be date inputs or filter inputs', 'errorMessage': 'must_be_date_inputs_or_filter_inputs'}: 필터 조건 없음
            400, {'message': 'must be other date input', 'errorMessage': 'must_be_other_date_input'} : 날짜 조건 없음
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            403, {'message': 'no permission to get order list', 'errorMessage': 'no_permission_to_get_order_list'} : 주문 리스트 조회 권한 없음
            404, {'message': 'order does not exist', 'errorMessage': 'order_does_not_exist'} : 주문 리스트 없음
            

        History:
            2020-12-29(김민서): 초기 생성
            2020-12-30(김민서): 1차 수정
            2020-12-31(김민서): 2차 수정
        """

        try:
            connection = get_connection(self.database)
            contexts = self.service.get_orders_service(connection, data)
            result = []

            for order_list in contexts['order_lists']:
                order_list['total_price'] = str(order_list['total_price'])
                order_list['option_extra_cost'] = str(order_list['option_extra_cost'])
                result.append(order_list)

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
        Param('status_id', PATH, int, required=True, rules=[OrderStatusRule()]),
        Param('id', GET, list, required=True)
    )
    def patch(self, *args):
        data = {
            'permission': g.permission_id,
            'account': g.acount_id,
            "status": args[0],
            "ids": args[1]
        }

        """PATCH 메소드: 주문 상태 변경

        Args: 
            args = ('status', 'ids')

        Author: 김민서

        Returns: { "message": "success" }

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'} : 잘못 입력된 키값        
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            400, {'message': 'now order status is not allowed to update status', 'errorMessage': 'now_order_status_is_not_allowed_to_update_status'}: 주문 상태 변경 불가능 상
            400, {'message': 'unable to update order status', 'errorMessage': 'unable_to_update_order_status'}: 수정 내역 없음
            403, {'message': 'no permission', 'errorMessage': 'no_permission'} : 주문 상태 변경 권한 없음

        History:
            2021-01-01(김민서): 초기 생성    
        """

        try:
            connection = get_connection(self.database)
            self.service.update_order_status_service(connection, data)
            connection.commit()
            return {'message': 'success'}

        except Exception as e:
            connection.rollback()
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')




