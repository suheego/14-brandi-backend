import json
from flask                   import jsonify, request
from flask.views             import MethodView

from utils.connection        import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.decorator         import signin_decorator
from utils.rules             import NumberRule, DefaultRule, EmailRule


from flask_request_validator import (
    Param,
    PATH,
    JSON,
    FORM,
    validate_params
)


class SellerSignupView(MethodView):
    def __init__(self, service, database):
        self.service = service
        self.database = database

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

    def __init__(self, services, database):
        self.service = services
        self.database = database

    @validate_params(
        Param('username', JSON, str),
        Param('password', JSON, str)
    )
    def post(self, *args):
        connection = None
        data = {
            'username': args[0],
            'password': args[1]
        }
        try:
            connection = get_connection(self.database)
            token = self.service.seller_signin_service(connection, data)
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

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('account_id', PATH, str, required=True, rules=[NumberRule()]),
    )
    def get(self, *args):
        """ GET 메소드: 셀러 상세정보 조회

            Author:
                이영주

            Returns:
                200, {'message': 'success', 'result': result}                                           : 상세정보 조회 성공

            Raises:
                400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
                400, {'message': 'seller does not exist error', 'errorMessage': 'seller_does_not_exist'}: 셀러 정보 조회 실패
                400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
                500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

            History:
                2020-12-28(이영주): 초기 생성
        """

        # @ 데코레이터
        data = {
            'account_id': args[0],
        }
        try:
            connection          = get_connection(self.database)
            result              = self.service.get_seller_info(connection, data)
            return jsonify({'message': 'success', 'result': result}), 200

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')

    @validate_params(
        # required True
        Param('profile_image_url', FORM, str, required=True, rules=[DefaultRule()]),
        Param('seller_title', FORM, str, required=True, rules=[DefaultRule()]),
        Param('contact_name', FORM, str, required=True, rules=[DefaultRule()]),
        Param('contact_phone', FORM, str, required=True, rules=[DefaultRule()]),
        Param('contact_email', FORM, str, required=True, rules=[DefaultRule()]),
        Param('service_center_number', FORM, str, required=True, rules=[DefaultRule()]),
        Param('post_number', FORM, str, required=True, rules=[DefaultRule()]),
        Param('address1', FORM, str, required=True, rules=[DefaultRule()]),
        Param('address2', FORM, str, required=True, rules=[DefaultRule()]),
        Param('operation_start_time', FORM, str, required=True),
        Param('operation_end_time', FORM, str, required=True),
        Param('shipping_information', FORM, str, required=True, rules=[DefaultRule()]),
        Param('exchange_information', FORM, str, required=True, rules=[DefaultRule()]),
        # required False
        Param('background_image_url', FORM, str, required=False, rules=[DefaultRule()]),
        Param('seller_discription', FORM, str, required=False, rules=[DefaultRule()]),
        Param('is_weekend', FORM, str, required=False, rules=[DefaultRule()]),
        Param('weekend_operation_start_time', FORM, str, required=False, rules=[DefaultRule()]),
        Param('weekend_operation_end_time', FORM, str, required=False, rules=[DefaultRule()]),
        # master
        Param('name', FORM, str, required=False, rules=[DefaultRule()]),
        Param('english_name', FORM, str, required=False, rules=[DefaultRule()]),
        # permission_type
        Param('account_id', FORM, str, required=True, rules=[DefaultRule()]),
        Param('permission_types', FORM, str, required=True, rules=[DefaultRule()]),
        # histories
        Param('seller_status_type_id', FORM, str, required=True, rules=[DefaultRule()]),
        Param('seller_id', FORM, str, required=True, rules=[DefaultRule()]),
        Param('updater_id', FORM, str, required=True, rules=[DefaultRule()])
    )
     # password 변경
    def patch(self, *args):
        """ PATCH 메소드: 셀러 정보 수정

            Author: 이영주

            Returns:
                200, {'message': 'success', 'result': result}                                           : 셀러 정보변경

            Raises:
                400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
                400, {'message': 'unable to update', 'errorMessage': 'unable_to_update'}                : 셀러 정보 수정 실패
                400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
                500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

            History:
                2020-12-29(이영주): 초기 생성
        """
        try:
            add_contact = json.loads(request.form.get("add_contact", "1"))
            data = {
                'profile_image_url': request.form.get('profile_image_url'),
                'background_image_url': request.form.get('background_image_url'),
                'seller_title': request.form.get('seller_title'),
                'seller_discription': request.form.get('seller_discription'),
                'contact_name': request.form.get('contact_name'),
                'contact_phone': request.form.get('contact_phone'),
                'contact_email': request.form.get('contact_email'),
                'post_number': request.form.get('post_number'),
                'service_center_number': request.form.get('service_center_number'),
                'address1': request.form.get('address1'),
                'address2': request.form.get('address2'),
                'operation_start_time': request.form.get('operation_start_time'),
                'operation_end_time': request.form.get('operation_end_time'),
                'is_weekend': request.form.get('is_weekend'),
                'weekend_operation_start_time': request.form.get('weekend_operation_start_time'),
                'weekend_operation_end_time': request.form.get('weekend_operation_end_time'),
                'shipping_information': request.form.get('shipping_information'),
                'exchange_information': request.form.get('exchange_information'),
                'name': request.form.get('name'),
                'english_name': request.form.get('english_name'),
                'account_id': request.form.get('account_id'),
                'permission_types': request.form.get('permission_types'),
                'seller_status_type_id': request.form.get('seller_status_type_id'),
                'seller_id': request.form.get('account_id'),
                'updater_id': request.form.get('permission_types'),
                'add_contact': add_contact
            }
            connection = get_connection(self.database)

            # master - update seller table
            self.service.patch_master_info(connection, data)

            # update sellers table
            self.service.patch_seller_info(connection, data)

            # update additional_contacts table
            self.service.patch_add_contact(connection, data)

            # update seller_histories
            self.service.patch_seller_history(connection, data)

            connection.commit()
            return jsonify({'message': 'success', 'result': data}), 200

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class SellerStatusView(MethodView):
    """ Presentation Layer
    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service : SellerInfoService 클래스

    Author:
        이영주

    History:
        2021-01-03(이영주): 초기 생성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database

    @validate_params(
        Param('account_id', JSON, str, required=True, rules=[DefaultRule()]),
        Param('seller_status_type_id', JSON, str, required=True, rules=[DefaultRule()]),
        Param('seller_id', JSON, str, required=True, rules=[DefaultRule()]),
        Param('updater_id', JSON, str, required=True, rules=[DefaultRule()])
    )
    def patch(self, *args):
        """PATCH 메소드:
                셀러 상태 정보 수정
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
            2021-01-03(이영주): 초기 생성
        """
        try:
            data = {
                'account_id': args[0],
                'seller_status_type_id': args[1],
                'seller_id': args[2],
                'updater_id': args[3]
            }
            connection = get_connection(self.database)
            self.service.patch_seller_status(connection, data)
            self.service.patch_seller_history(connection, data)
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
            'account_id': args[0]
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

class SellerPasswordView(MethodView):
    """ Presentation Layer

        Attributes:
            database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
            service : SellerPasswordService 클래스

        Author:
            이영주

        History:
            2021-01-04(이영주): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    # @signin_decorator
    @validate_params(
        Param('account_id', JSON, str, required=False, rules=[DefaultRule()]),
        Param('password', JSON, str, required=False, rules=[DefaultRule()])
    )
    def patch(self, *args):
        """PATCH 메소드:
                셀러 비밀번호 수정
        Author:
            이영주

        Returns:
            200, {'message': 'success'}                                                             : 셀러 정보변경

        # Raises:
        #     400, {'message': 'key error', 'errorMessage': 'key_error'}                              : 잘못 입력된 키값
        #     400, {'message': 'unable to update', 'errorMessage': 'unable_to_update'}                : 셀러 정보 수정 실패
        #     400, {'message': 'unable to close database', 'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
        #     500, {'message': 'internal server error', 'errorMessage': format(e)})                   : 서버 에러

        History:
            2021-01-04(이영주): 초기 생성
        """
        try:
            data = {
                'account_id': args[0],
                'password': args[1]
            }
            connection = get_connection(self.database)
            self.service.patch_seller_password(connection, data)
            return jsonify({'message': 'success', 'result': 'PasswordChange'}), 200

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
