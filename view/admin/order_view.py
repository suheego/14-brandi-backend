from flask import jsonify, g
from flask.views import MethodView

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import OrderStatusRule, DateTimeRule, NumberRule, PhoneRule, PageRule, DateRule

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
        Param('status', GET, int, rules=[OrderStatusRule()]),
        Param('number', GET, str, required=False),
        Param('detail_number', GET, str, required=False),
        Param('sender_name', GET, str, required=False),
        Param('sender_phone', GET, str, required=False, rules=[NumberRule], default=''),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('start_date', GET, str, required=False, rules=[DateRule()], default=''),
        Param('end_date', GET, str, required=False, rules=[DateRule()], default=''),
        Param('attributes', GET, list, required=False),
        Param('order_by', GET, str, required=False),
        Param('page', GET, int, rules=[PageRule()]),
        Param('length', GET, str, rules=[NumberRule()])
    )
    def get(self, *args):
        data = {
            'permission': 1,
            'account': 1,
            #'permission': g.permission_id,
            #'account': g.acount_id,
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
        print(data)
        try:
            connection = get_connection(self.database)

            contexts = self.service.get_orders_service(connection, data)
            result = []

            for order_list in contexts['order_lists']:
                order_list['total_price'] = str(order_list['total_price'])
                order_list['option_extra_cost'] = str(order_list['option_extra_cost'])
                result.append(order_list)

            return jsonify({'message': 'success', 'totalCount': contexts['total_count'], 'results': result}), 200
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('status_id', PATH, int, rules=[OrderStatusRule()]),
        Param('id', GET, list)
    )
    def patch(self, *args):
        data = {
            #'permission': g.permission_id,
            #'account': g.acount_id,
            'permission': 1,
            'account': 1,
            "status": args[0],
            "ids": args[1]
        }
        print(data['ids'])

        """PATCH 메소드: 주문 상태 변경

        Args: 
            args = ('status', 'ids')

        Author: 김민서

        Returns: { "message": "success" }

        Raises:
            400, {'message': 'key error', 
                    'errorMessage': 'key_error'} : 잘못 입력된 키값
                            
            400, {'message': 'unable to close database', 
                    'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
                    
            400, {'message': 'now order status is not allowed to update status', 
                    'errorMessage': 'now_order_status_is_not_allowed_to_update_status'}: 주문 상태 변경 불가능 상태
                    
            403, {'message': 'no permission', 
                    'errorMessage': 'no_permission'} : 권한 없음

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


class OrderDetailView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('order_item_id', PATH, str, rules=[NumberRule()])
    )
    def get(self, *args):
        data = {
            #"permission": g.permission_id,
            "permission": 1,
            "order_item_id": args[0]
        }

        """GET 메소드: 주문 상세 정보 조회     

        Args: 
            args = ('order_item_id')

        Author: 김민서

        Returns: 
            {
                "message": "success",
                "result": {
                    "order_detail_info": [
                        {
                            "customer_phone": "12345667890",
                            "order_detail_number": "oidt00001",
                            "order_item_id": 1,
                            "order_item_purchased_date": "2020-12-31 13:25:03",
                            "status": "배송중"
                        }
                    ],
                    "order_info": [
                        {
                            "order_id": 1,
                            "order_number": "20201225000000001",
                            "order_purchased_date": "2020-12-31 13:25:03",
                            "total_price": 18000.0
                        }
                    ],
                    "order_status_history": [
                        {
                            "date": "2021-01-03 01:26:05",
                            "status": "배송중"
                        },
                        {
                            "date": "2020-12-31 13:25:01",
                            "status": "상품준비"
                        }
                    ],
                    "product_info": [
                        {
                            "brand_name": "나는셀러3",
                            "discount_rate": 0.1,
                            "option_information": "Black/Free",
                            "price": "10000 원 (할인가 9000원)",
                            "product_name": "성보의하루1",
                            "product_number": "P0000000000000000001",
                            "qauntity": 1
                        }
                    ],
                    "recipient_info": [
                        {
                            "customer_name": "user1",
                            "delivery_memo": "문 앞에 놓아주세요",
                            "destination": "서울시 강남 위코드 아파 (123321)",
                            "recipient_name": "둘리",
                            "recipient_phone": "01022222222",
                            "user_id": 102
                        }
                    ],
                    "updated_at_time": "2021-01-03 00:42:12"
                }
            }
            
        Raises:
            400, {'message': 'key error',
                    'errorMessage': 'key_error'} : 잘못 입력된 키값
                    
            400, {'message': 'does not exist order detail',
                    'errorMessage': 'does_not_exist_order_detail'} : 주문 상세 정보 없음
                    
            403, {'message': 'no permission',
                     'errorMessage': 'no_permission'} : 권한 없음
                        
            400, {'message': 'unable to close database',
                    'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            
        History:
            2021-01-01(김민서): 초기 생성    
        """

        try:
            connection = get_connection(self.database)
            result = self.service.get_order_detail_service(connection, data)

            return {"message": "success", "result": result}
        except Exception as e:
            raise e
        finally:
            try:
                connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


    @validate_params(
        Param('order_item_id', GET, str, rules=[NumberRule()]),
        Param("updated_at_time", GET, str, rules=[DateTimeRule()]),
        Param("sender_phone", GET, str, required=False, rules=[PhoneRule()]),
        Param("recipient_phone", GET, str, required=False, rules=[PhoneRule()]),
        Param("address1", GET, str, required=False),
        Param("address2", GET, str, required=False)
    )
    def patch(self, *args):
        data = {
            # "permission": g.permission_id,
            "permission": 1,
            "order_item_id": args[0],
            "updated_at_time": args[1],
            "sender_phone": args[2],
            "recipient_phone": args[3],
            "address1": args[4],
            "address2": args[5]
        }

        """PATCH 메소드: 주문 상세 정보 수정     

        Args: 
            args = ('order_item_id', 'updated_at_time', 'sender_phone', 'recipient_phone', 'address1', 'address2')

        Author: 김민서

        Returns: {'message': 'success'}

        Raises:
            400, {'message': 'key error', 
                    'errorMessage': 'key_error'} : 잘못 입력된 키값
                    
            400, {'message': 'unable to close database', 
                    'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
                    
            403, {'message': 'no permission', 
                    'errorMessage': 'no_permission'} : 권한 없음
                    
            400, {'message': input does not exists, 
                    'errorMessage': 'input_does_not_exists'} : 수정 정보 존재하지 않음
                    
            400, {'message': 'one of address inputs does not exist', 
                    'errorMessage': 'one_of_address_inputs_does_not_exist'} : 수정할 주소 정보 부족
                    
            400, {'message': 'unable to update', 
                    'errorMessage': 'unable_to_update'} : 수정 불가       
            

        History:
            2021-01-01(김민서): 초기 생성    
        """

        try:
            connection = get_connection(self.database)
            self.service.update_order_detail_service(connection, data)
            connection.commit()
            return {"message": "success"}
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            try:
                connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
