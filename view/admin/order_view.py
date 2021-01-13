from flask import jsonify, g
from flask.views import MethodView

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import SecondDateTimeRule, NumberRule, PhoneRule, PageRule, DateRule
from utils.decorator import signin_decorator

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

    @signin_decorator()
    @validate_params(
        Param('status', GET, int),
        Param('number', GET, str, required=False),
        Param('detail_number', GET, str, required=False),
        Param('sender_name', GET, str, required=False),
        Param('sender_phone', GET, str, required=False),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('start_date', GET, str, required=False, rules=[DateRule()]),
        Param('end_date', GET, str, required=False, rules=[DateRule()]),
        Param('attributes', GET, list, required=False),
        Param('order_by', GET, str, required=False),
        Param('page', GET, int, rules=[PageRule()]),
        Param('length', GET, str, rules=[NumberRule()])
    )
    def get(self, *args):
        data = {
            'permission': g.permission_type_id,
            'account': g.account_id,
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
            400, {'message': 'key_error', 
                'errorMessage': 'key error'} : 잘못 입력된 키값
                
            400, {'message': 'must_be_date_inputs_or_filter_inputs', 
                'errorMessage': '검색어 조건과 날짜 조건 둘 중에 하나는 반드시 포함되어야 합니다.'}: 필터 조건 없음
                
            400, {'message': 'must_be_other_date_input', 
                'errorMessage': '시작일과 마지막일이 모두 포함되어야 합니다.'} : 날짜 조건 없음
                
            400, {'message': 'end_date_is_invalid', 
                'errorMessage': '시작일이 마지막일보다 늦습니다.'} : 시작일이 마지막일보다 늦음

            400, {'message': 'unable_to_close_database', 
                'errorMessage': 'unable to close database'}: 커넥션 종료 실패
                
            403, {'message': 'no_permission', 
                'errorMessage': '권한이 없습니다.'} : 주문 리스트 조회 권한 없음
                
            400, {'message': 'order_does_not_exist', 
                'errorMessage': '주문 내역이 없습니다.'} : 주문 리스트 없음
                
            500, {'message': 'internal_server_error',
                     'errorMessage': 'internal server error'} : 알 수 없는 에러
            

        History:
            2020-12-29(김민서): 초기 생성
            2020-01-03(김민서): 1차 수정
        """

        try:
            connection = get_connection(self.database)
            result = self.service.get_orders_service(connection, data)
            return jsonify({'message': 'success', 'totalCount': result['total_count'], 'results': result['order_lists']}), 200
        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @signin_decorator()
    @validate_params(
        Param('status_id', JSON, int),
        Param('ids', JSON, list)
    )
    def patch(self, *args):
        data = {
            'permission': g.permission_type_id,
            'account': g.account_id,
            "status": args[0],
            "ids": args[1]
        }
        
        """PATCH 메소드: 주문 상태 변경

        Args: 
            args = ('status', 'ids')

        Author: 김민서

        Returns: { "message": "주문 상태가 업데이트 되었습니다." }

        Raises:
            400, {'message': 'key error', 
                    'errorMessage': 'key_error'} : 잘못 입력된 키값
                            
            400, {'message': 'unable to close database', 
                    'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
                    
            400, {'message': 'now order status is not allowed to update status', 
                    'errorMessage': '현재 상태는 업데이트가 불가합니다.'}: 주문 상태 변경 불가능 상태
                    
            400, {'message': 'unable_to_update_status', 
                    'errorMessage': '업데이트가 불가합니다.'}: 수정 불가
                    
            403, {'message': 'no_permission', 
                    'errorMessage': '권한이 없습니다.'} : 권한 없음
                    
            500, {'message': 'internal_server_error',
                     'errorMessage': 'internal server error'} : 알 수 없는 에러

        History:
            2021-01-01(김민서): 초기 생성
            2021-01-12(김민서): 1차 수정    
        """

        try:
            connection = get_connection(self.database)
            self.service.update_order_status_service(connection, data)
            connection.commit()
            return jsonify({'message': '주문 상태가 업데이트 되었습니다.'}), 200

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

    @signin_decorator()
    @validate_params(
        Param('order_item_id', PATH, int)
    )
    def get(self, *args):
        data = {
            "permission": g.permission_type_id,
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
            400, {'message': 'key_error',
                    'errorMessage': 'key error'} : 잘못 입력된 키값
                    
            400, {
                    "error_message:": "order_item_id이 유효하지 않습니다.",
                    "message": {
                        "order_item_id": [
                            "Value is required"
                        ]
                    }
                } : 필수 입력값 없음
                    
            400, {'message': 'does_not_exist_order_detail',
                    'errorMessage': '주문 상세 정보가 존재하지 않습니다.'} : 주문 상세 정보 없음
                    
            403, {'message': 'no_permission',
                     'errorMessage': '권한이 없습니다.'} : 권한 없음
                        
            400, {'message': 'unable_to_close_database',
                    'errorMessage': 'unable to close database'}: 커넥션 종료 실패
                    
            500, {'message': 'internal_server_error',
                     'errorMessage': 'internal server error'} : 알 수 없는 에러
            
        History:
            2021-01-01(김민서): 초기 생성    
        """

        try:
            connection = get_connection(self.database)
            result = self.service.get_order_detail_service(connection, data)
            return jsonify({"message": "success", "result": result}), 200
        except Exception as e:
            raise e
        finally:
            try:
                connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
            

    @signin_decorator()
    @validate_params(
        Param('order_item_id', JSON, str, rules=[NumberRule()]),
        Param("updated_at_time", JSON, str, rules=[SecondDateTimeRule()]),
        Param("sender_phone", JSON, str, required=False, rules=[PhoneRule()]),
        Param("recipient_phone", JSON, str, required=False, rules=[PhoneRule()]),
        Param("address1", JSON, str, required=False),
        Param("address2", JSON, str, required=False)
    )
    def patch(self, *args):
        data = {
            "permission": g.permission_type_id,
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
            400, {'message': 'key_error', 
                    'errorMessage': 'key error'} : 잘못 입력된 키값
                    
            400, {'message': 'unable_to_close_database', 
                    'errorMessage': 'unable to close database'}: 커넥션 종료 실패
                    
            403, {'message': 'no_permission', 
                    'errorMessage': '권한이 없습니다.'} : 권한 없음
                    
            400, {'message': input_does_not_exist, 
                    'errorMessage': '수정 정보가 없습니다.'} : 수정 정보 존재하지 않음
                    
            400, {'message': 'one_of_address_inputs_does_not_exist', 
                    'errorMessage': '수정 주소 정보가 누락되었습니다.'} : 수정할 주소 정보 부족
                    
            400, {'message': 'unable_to_update', 
                    'errorMessage': '업데이트가 불가합니다.'} : 수정 불가   
                    
            400, {'message': 'denied_to_update', 
                    'errorMessage': '업데이트가 실행되지 않았습니다.'} : 수정 실패
                    
            500, {'message': 'internal_server_error',
                     'errorMessage': 'internal server error'} : 알 수 없는 에러
                    

        History:
            2021-01-01(김민서): 초기 생성
            2021-01-12(김민서): 1차 수정    
        """

        try:
            connection = get_connection(self.database)
            self.service.update_order_detail_service(connection, data)
            connection.commit()
            return jsonify({"message": "success"}), 200
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            try:
                connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
