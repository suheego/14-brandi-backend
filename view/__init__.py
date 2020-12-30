""" 엔드 포인트의 시작 및 URL 관리

create_endpoints 함수가 정의되어 있는 곳. 함수 안에 사용할 url endpoint 를 정의한다.
파일 끝에 error_handle()함수를 호출 한다.

기본적인 사용 예시:
    app.add_url_rule('/test', view_func=TestUserView.as_view('test_user_view', test_user_service, database))

"""


from .sample_user_view import SampleUserView
from .store.user_view import SignUpView, SignInView, GoogleSocialSignInView
from .store.destination_view import DestinationView, DestinationDetailView
from .store.cart_item_view import CartItemView, CartItemAddView
from utils.error_handler import error_handle


def create_endpoints(app, services, database):
    """ 앤드 포인트 시작

        Args:
            app     : Flask 앱
            services: Services 클래스:Service 클래스들을 담고 있는 클래스이다.
            database: 데이터베이스

        Author: 홍길동

        Returns: None

        Raises: None
            
        History:
            2020-20-20(홍길동): 초기 생성
            2020-20-21(홍길동): 1차 수정
            2020-20-22(홍길동): 2차 수정
    """
    sample_user_service = services.sample_user_service
    user_service = services.user_service
    destination_service = services.destination_service
    cart_item_service = services.cart_item_service
    
# ----------------------------------------------------------------------------------------------------------------------
# Service Section(write your code under your name)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# 김기용 example ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------

    # services 넘겨주기...
    app.add_url_rule('/test',
                     view_func=SampleUserView.as_view(
                         'sample_user_view',
                         sample_user_service,
                         database
                     ))

    # destination 상세 정보 불러오기
    app.add_url_rule('/destination/<destination_id>',
                     view_func=DestinationDetailView.as_view(
                         'destination_detail_view',
                         destination_service,
                         database
                     ))

    # destination view
    app.add_url_rule('/destination',
                     view_func=DestinationView.as_view(
                         'destination_View',
                         destination_service,
                         database
                     ))

# ----------------------------------------------------------------------------------------------------------------------
# 김민구 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------
    app.add_url_rule('/users/signup',
                     view_func=SignUpView.as_view(
                         'sign_up_view',
                         user_service,
                         database
                     ))

    app.add_url_rule('/users/signin',
                     view_func=SignInView.as_view(
                         'sign_in_view',
                         user_service,
                         database
                     ))

    app.add_url_rule('/users/social',
                     view_func=GoogleSocialSignInView.as_view(
                         'google_social_sign_in_view',
                         user_service,
                         database
                     ))






# ----------------------------------------------------------------------------------------------------------------------
# 고수희
# ----------------------------------------------------------------------------------------------------------------------
    app.add_url_rule('/checkout/cart',
                    view_func=CartItemAddView.as_view(
                        'cart_item_add_view',
                        cart_item_service,
                        database
                    ))

    app.add_url_rule('/checkout/cart/<int:cart_id>',
                    view_func=CartItemView.as_view(
                        'cart_item_view',
                        cart_item_service,
                        database
                    ))

# ----------------------------------------------------------------------------------------------------------------------
# Admin 1 Section
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# 이영주 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Admin 2 Section
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# 이성보 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    # don't touch this
    error_handle(app)
# ----------------------------------------------------------------------------------------------------------------------
