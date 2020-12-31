""" 엔드 포인트의 시작 및 URL 관리

create_endpoints 함수가 정의되어 있는 곳. 함수 안에 사용할 url endpoint 를 정의한다.
파일 끝에 error_handle()함수를 호출 한다.

기본적인 사용 예시:
    app.add_url_rule('/test', view_func=TestUserView.as_view('test_user_view', test_user_service, database))

"""
from .sample_user_view import SampleUserView

from .admin.order_view import OrderView
from .admin.event_view import EventView, EventDetailView
from .admin.seller_view import SellerSignupView, SellerSigninView
from .admin.create_product_view import CreateProductView

from .store.user_view import SignUpView, SignInView, GoogleSocialSignInView
from .store.product_list_view import ProductListView, ProductSearchView, ProductDetailView
from .store.category_list_view import CategoryListView
from .store.destination_view import DestinationView, DestinationDetailView
from .store.cart_item_view import CartItemView, CartItemAddView
from .store.sender_view import SenderView
from .store.store_order_view import StoreOrderView, StoreOrderAddView

from utils.error_handler import error_handle

def create_endpoints(app, services, database):
    sample_user_service = services.sample_user_service

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
    destination_service = services.destination_service
    cart_item_service = services.cart_item_service
    sender_service = services.sender_service
    product_list_service = services.product_list_service
    store_order_service = services.store_order_service

    seller_service = services.seller_service
    create_product_service = services.create_product_service
    order_service = services.order_service


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

    # product_detail_view
    app.add_url_rule('/products/<product_id>',
                     view_func=ProductDetailView.as_view(
                         'product_detail_view',
                         product_list_service,
                         database
                     ))
    # product_search
    app.add_url_rule('/products/search',
                     view_func=ProductSearchView.as_view(
                         'product_search',
                         product_list_service,
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
                         services,
                         database
                     ))

    app.add_url_rule('/users/signin',
                     view_func=SignInView.as_view(
                         'sign_in_view',
                         services,
                         database
                     ))

    app.add_url_rule('/users/social-signin',
                     view_func=GoogleSocialSignInView.as_view(
                         'google_social_sign_in_view',
                         services,
                         database
                     ))

    app.add_url_rule('/products',
                     view_func=ProductListView.as_view(
                         'product_list_view',
                         services,
                         database
                     ))

    app.add_url_rule('/categories',
                     view_func=CategoryListView.as_view(
                         'category_list_view',
                         services,
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

    app.add_url_rule('/checkout/sender',
                    view_func=SenderView.as_view(
                        'sender_view',
                        sender_service,
                        database
                    ))

    app.add_url_rule('/checkout',
                     view_func=StoreOrderAddView.as_view(
                        'store_order_add_view',
                        store_order_service,
                        database
                    ))

    app.add_url_rule('/checkout/<int:order_id>',
                    view_func=StoreOrderView.as_view(
                        'store_order_view',
                        store_order_service,
                        database
                    ))

# ----------------------------------------------------------------------------------------------------------------------
# Admin 1 Section
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# 강두연 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------
    app.add_url_rule('/events',
                     view_func=EventView.as_view(
                         'event_view',
                         services.event_service,
                         database
                     ))

    app.add_url_rule('/event/<int:event_id>',
                     view_func=EventDetailView.as_view(
                         'event_detail_view',
                         services.event_service,
                         database
                     ))

# ----------------------------------------------------------------------------------------------------------------------
# 김민서 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------
    app.add_url_rule('/admin/orders',view_func=OrderView.as_view('order_view', order_service, database))

# ----------------------------------------------------------------------------------------------------------------------
# 이성보 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Admin 2 Section
# ----------------------------------------------------------------------------------------------------------------------
# 김영환
    app.add_url_rule('/admin/signup',
                     view_func = SellerSignupView.as_view(
                         'seller_signup_view',
                         seller_service,
                         database
                     ))
    app.add_url_rule('/admin/signin',
                     view_func = SellerSigninView.as_view(
                         'seller_signin_view',
                         seller_service,
                         database
                     ))

# ----------------------------------------------------------------------------------------------------------------------
# 심원두
    app.add_url_rule('/product/productRegist',
                     view_func=CreateProductView.as_view(
                         'create_product_view',
                         create_product_service,
                         database
                     ))
# ----------------------------------------------------------------------------------------------------------------------
# 이성보 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# 이영주 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# 장재원 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
    # don't touch this
    error_handle(app)
# ----------------------------------------------------------------------------------------------------------------------
