import json
from flask                   import jsonify, request
from flask.views             import MethodView

from utils.connection        import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules             import NumberRule, DefaultRule, EmailRule

from flask_request_validator import (
    Param,
    PATH,
    JSON,
    FORM,
    GET,
    validate_params
)

class SellerSearchView(MethodView):
  
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('page', GET, int, required=False),
        Param('page_view', GET, int, required=False),
        Param('account_id', JSON, int, required=False),
        Param('username', JSON, str, required=False),
        Param('seller_english_name', JSON, str, required=False),
        Param('seller_name', JSON, str, required=False),
        Param('contact_name', JSON, str, required=False),
        Param('contact_phone', JSON, str, required=False),
        Param('contact_email', JSON, str, required=False),
        Param('seller_attribute_type_name', JSON, str, required=False),
        Param('seller_status_type_name', JSON, str, required=False),
        Param('updated_at', JSON, str, required=False),
        Param('start_date',JSON, str, required=False),
        Param('end_date', JSON, str, required=False)
    )

    def get(self, *args):
        try:
            data = {
                'account_id' : args[2],
                'username' : args[3],
                'seller_english_name' : args[4],
                'seller_name': args[5],
                'contact_name': args[6],
                'contact_phone': args[7],
                'contact_email': args[8],
                'seller_attribute_type_name': args[9],
                'seller_status_type_name': args[10],
                'updated_at': args[11],
                'start_date': args[12],
                'end_date' : args[13]
            }

            page = request.args.get('page',1)
            page_view = request.args.get('page_view',10)

            connection = get_connection(self.database)
            seller_list = self.service.seller_search_service(connection, data, page, page_view)
            return jsonify({'message':'success', 'result': seller_list}),200

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail in seller_list_view')

class SellerSignupView(MethodView):

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str),
        Param('seller_attribute_type_id', JSON, str),
        Param('name', JSON, str),
        Param('english_name', JSON, str),
        Param('contact_phone', JSON, str),
        Param('service_center_number', JSON, str),
    )
    def post(self, *args):

        data = {
            'username' : args[0],
            'password' : args[1],
            'seller_attribute_type_id': args[2],
            'name': args[3],
            'english_name': args[4],
            'contact_phone': args[5],
            'service_center_number': args[6],
        }

        try:
            connection = get_connection(self.database)
            self.service.seller_signup_service(connection,data)
            connection.commit()
            return jsonify({'message': 'success'}),200


        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class SellerSigninView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str)
    )
    def post(self, *args):
        data = {
            'username': args[0],
            'password': args[1]
        }

        try:
            connection = get_connection(self.database)
            token = self.service.seller_signin_service(connection, data)
            connection.commit()
            return jsonify({'message':'login success','token': token}),200

        except Exception as e:
            connection.rollback()                


class SellerInfoView(MethodView):
    """ Presentation Layer
    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service : SellerInfoService 클래스

    Author:
        이영주

    History:
        2020-12-28(이영주): 초기 생성
    """
    @validate_params(
      Param('account_id', PATH, str, required=True, rules=[NumberRule()])
    )
    def get(self, *args):
        """GET 메소드:
            해당 셀러의 정보를 조회.
            account_id 에 해당되는 셀러를 테이블에서 조회 후 가져온다.
        Args:
            account_id
        Author:
            이영주

        Returns:
            result seller

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'seller does not exist error', 'errorMessage': 'seller_does_not_exist'}: 셀러 정보 조회 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-28(이영주): 초기 생성
        """
        data = {
            'account_id': args[0]
        }
        try:
            connection = get_connection(self.database)
            seller = self.service.get_seller_info(connection, data)
            return jsonify({'message' : 'success', 'result' : seller}), 200

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        Param('id', FORM, str, rules=[NumberRule()]),

        Param('id', JSON, str, rules=[NumberRule()]),
        Param('name', JSON, str, rules=[DefaultRule()]),
        Param('phone', JSON, str, rules=[NumberRule()]),
        Param('email', JSON, str, rules=[EmailRule()]),
        Param('order_index', JSON, str, rules=[NumberRule()]),
        Param('seller_id', JSON, str, rules=[NumberRule()]),
        Param('contact_name', JSON, str, required=False, rules=[DefaultRule()]),
        Param('contact_phone', JSON, str, required=False, rules=[NumberRule()]),
        Param('contact_email', JSON, str, required=False, rules=[EmailRule()]),
    )
    def post(self, *args):
        """POST 메소드:
                추가 담당자 생성

        Args:



        Author:
            이영주

        Returns:
            200, {'message': 'success'}                                                             : 유저 생성 성공

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'user create error', 'errorMessage': 'user_create_error'}              : 유저 생성 실패
            403, {'message': 'user already exist', errorMessage': 'already_exist'}                  : 중복 유저 생성 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-30(이영주): 초기 생성
        """
        data = {
            'id': args[0],
            'name': args[1],
            'phone': args[2],
            'email': args[3],
            'order_index': args[4],
            'seller_id': args[5],
            'contact_name': args[6],
            'contact_phone': args[7],
            'contact_email': args[8]
        }

        try:
            connection = get_connection(self.database)
            self.service.post_person_in_charge(connection, data)
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

    @validate_params(
        Param('id', FORM, str, required=True, rules=[DefaultRule()]),
        Param('name', FORM, str, required=True, rules=[DefaultRule()]),
        Param('english_name', FORM, str, required=True, rules=[DefaultRule()]),
        Param('seller_title', FORM, str, required=True, rules=[DefaultRule()]),
        Param('seller_discription', FORM, str, required=True, rules=[DefaultRule()]),
        Param('contact_name', FORM, str, required=True, rules=[DefaultRule()]),
        Param('contact_email', FORM, str, required=True, rules=[DefaultRule()]),
        Param('contact_phone', FORM, str, required=True, rules=[DefaultRule()]),
        Param('post_number', FORM, str, required=True, rules=[DefaultRule()]),
        Param('service_center_number', FORM, str, required=True, rules=[DefaultRule()]),
        Param('address1', FORM, str, required=True, rules=[DefaultRule()]),
        Param('address2', FORM, str, required=True, rules=[DefaultRule()]),
        Param('operation_start_time', FORM, str, required=True, rules=[DefaultRule()]),
        Param('operation_end_time', FORM, str, required=True, rules=[DefaultRule()]),
        Param('is_weekend', FORM, str, required=True, rules=[DefaultRule()]),
        Param('weekend_operation_start_time', FORM, str, required=True, rules=[DefaultRule()]),
        Param('weekend_operation_end_time', FORM, str, required=True, rules=[DefaultRule()]),
        Param('shipping_information', FORM, str, required=True, rules=[DefaultRule()]),
        Param('exchange_information', FORM, str, required=True, rules=[DefaultRule()])
    )
    def patch(self, *args):
        """PATCH 메소드:
                셀러 정보 수정
        Args:

        Author:
            이영주

        Returns:
            200, {'message': 'success'}                                                             : 셀러 정보변경

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'unable to update', 'errorMessage': 'unable_to_update'}                : 셀러 정보 수정 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-29(이영주): 초기 생성
        """
        data = {
            'account_id': args[0],
            'seller_discription': args[1],
            'seller_title': args[2],
            'status_id': args[3],
            'contact_name': args[5],
            'contact_phone': args[6],
            # 'additional_contact_info': args[8],
        }

        additional_contact_info = json.loads(request.form.get('additional_contact_info'))
        profile_image = request.files.get('profile_image')
        background_image = request.files.get('background_image', None)

        # data1 = {
        #     'id': request.form.get('id'),
        #
        # }

        try:
            print(data)
            print(profile_image)
            print(background_image)
            print(additional_contact_info)

            connection = get_connection(self.database)

            # update sellers table
            # self.service.patch_seller_info(connection, data)

            # update additional_contacts table
            # self.service.patch_seller_info(connection, data)

            # update seller_historiess
            # self.service.patch_seller_info(connection, data)

            # if permission_type_id == 1:
                # update seller_attribute_types table
                # self.service.patch_seller_info(connection, data)


            connection.commit()
            return jsonify({'message': 'success'}), 200

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class SellerHistoryView(MethodView):

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('account_id', PATH, str, required=False, rules=[NumberRule()])
    )
    def get(self, *args):
        """GET 메소드: 해당 셀러의 히스토리 정보를 조회.

        account_id 에 해당되는 셀러 히스토리를 테이블에서 조회 후 가져온다.

        Args:
            args = (account_id)

        Author:
            이영주

        Returns:
            seller_history

        Raises:
            400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
            400, {'message': 'seller does not exist error', 'errorMessage': 'seller_does_not_exist'}: 셀러 정보 조회 실패
            400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2020-12-28(이영주): 초기 생성
        """
        data = {
            'account_id' : args[0]
        }
        try:
            connection = get_connection(self.database)
            seller_history = self.service.get_seller_history(connection, data)
            return jsonify({'message' : 'success', 'result' : seller_history}), 200

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:

                raise DatabaseCloseFail('database close fail')