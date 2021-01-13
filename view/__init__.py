""" 엔드 포인트의 시작 및 URL 관리

create_endpoints 함수가 정의되어 있는 곳. 함수 안에 사용할 url endpoint 를 정의한다.
파일 끝에 error_handle()함수를 호출 한다.

기본적인 사용 예시:
    app.add_url_rule('/test', view_func=TestUserView.as_view('test_user_view', test_user_service, database))

"""

# service
from .sample_user_view         import SampleUserView
from .store.user_view          import SignUpView, SignInView, GoogleSocialSignInView
from .store.product_list_view  import ProductListView, ProductSearchView, ProductDetailView
from .store.category_list_view import CategoryListView
from .store.destination_view import DestinationView, DestinationDetailView
from .store.cart_item_view import CartItemView, CartItemAddView
from .store.sender_view import SenderView
from .store.store_order_view import StoreOrderView, StoreOrderAddView
from .store.bookmark_view import BookmarkView
from .store.event_list_view import EventBannerListView, EventDetailInformationView, EventDetailProductListView, EventDetailButtonListView
from .store.product_enquiry_view import ProductEnquiryListView, MyPageEnquiryListView
from .store.seller_shop_view import SellerShopView, SellerShopSearchView, SellerShopCategoryView, SellerShopProductListView

# admin1
from .admin.order_view import OrderView, OrderDetailView, OrderExcelView
from .admin.event_view import EventView, EventDetailView, EventProductsCategoryView, EventProductsToAddView
from .admin.enquiry_view import EnquiryView, AnswerView

# admin2

from .admin.seller_view import SellerSignupView, SellerSigninView, SellerInfoView, SellerHistoryView, SellerStatusView, \
    SellerPasswordView, SellerSearchView, SellerListView
from .admin.product_create_view import MainCategoriesListView, CreateProductView
from .admin.product_manage_view import ProductManageSearchView, ProductManageDetailView


from utils.error_handler import error_handle


def create_endpoints(app, services, database):

    """ 앤드 포인트 시작

            Args:
                app     : Flask 앱
                services: Services 클래스:Service 클래스들을 담고 있는 클래스이다.
                database: 데이터베이스

            Author: 김기용

            Returns: None

            Raises: None

            History:
                2020-12-28(김기용): 초기 생성
                2020-12-29(김기용): 1차 수정
                2020-12-31(강두연): 2차 수정
                2020-12-31(심원두): 3차 수정
    """

    # service
    sample_user_service  = services.sample_user_service
    destination_service  = services.destination_service
    cart_item_service    = services.cart_item_service
    sender_service       = services.sender_service
    product_list_service = services.product_list_service
    store_order_service  = services.store_order_service
    seller_shop_service = services.seller_shop_service
    seller_service = services.seller_service

    # admin1
    order_service = services.order_service
    order_detail_service = services.order_detail_service
    order_excel_service = services.order_excel_service

    # admin2
    seller_service         = services.seller_service
    seller_info_service    = services.seller_info_service
    product_create_service = services.product_create_service
    product_manage_service = services.product_manage_service

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

    app.add_url_rule('/products/<int:product_id>/bookmarks',
                     view_func=BookmarkView.as_view(
                         'bookmark_view',
                         services,
                         database
                     ))

    app.add_url_rule('/event-list',
                     view_func=EventBannerListView.as_view(
                        'event_banner_list_view',
                        services,
                        database
                     ))

    app.add_url_rule('/event-list/<int:event_id>',
                     view_func=EventDetailProductListView.as_view(
                        'event_detail_list_view',
                        services,
                        database
                     ))

    app.add_url_rule('/event-list/<int:event_id>/information',
                     view_func=EventDetailInformationView.as_view(
                        'event_detail_information',
                        services,
                        database
                     ))

    app.add_url_rule('/event-list/<int:event_id>/buttons',
                     view_func=EventDetailButtonListView.as_view(
                        'event_detail_button_list_view',
                        services,
                        database
                     ))

    app.add_url_rule('/products/<int:product_id>/enquiries',
                     view_func=ProductEnquiryListView.as_view(
                         'product_enquiry_view',
                         services,
                         database
                     ))

    app.add_url_rule('/users/my-page/enquiries',
                     view_func=MyPageEnquiryListView.as_view(
                         'my_page_enquiry_view',
                         services,
                         database
                     ))

# ----------------------------------------------------------------------------------------------------------------------
# 고수희
# ----------------------------------------------------------------------------------------------------------------------
    #장바구니 상품 추가 엔드포인트
    app.add_url_rule('/checkout/cart',
                     view_func=CartItemAddView.as_view(
                         'cart_item_add_view',
                         cart_item_service,
                         database
                     ))

    # 장바구니 상품 조회 엔드포인트
    app.add_url_rule('/checkout/cart/<int:cart_id>',
                     view_func=CartItemView.as_view(
                         'cart_item_view',
                         cart_item_service,
                         database
                     ))

    # 주문자 정보 조회 엔드포인트
    app.add_url_rule('/checkout/sender',
                    view_func=SenderView.as_view(
                        'sender_view',
                        sender_service,
                        database
                    ))

    # 상품 결제 엔드포인트
    app.add_url_rule('/checkout',
                     view_func=StoreOrderAddView.as_view(
                        'store_order_add_view',
                        store_order_service,
                        database
                    ))

    # 상품 결제 조회 엔드포인트
    app.add_url_rule('/checkout/<int:order_id>',
                    view_func=StoreOrderView.as_view(
                        'store_order_view',
                        store_order_service,
                        database
                    ))

    # 셀러샵 셀러 정보 조회 엔드포인트
    app.add_url_rule('/shops/<int:seller_id>',
                    view_func=SellerShopView.as_view(
                        'seller_shop_view',
                        seller_shop_service,
                        database
                    ))

    # 셀러샵 셀러 상품 검색 엔드포인트
    app.add_url_rule('/shops/<int:seller_id>/search',
                    view_func=SellerShopSearchView.as_view(
                        'seller_shop_search_view',
                        seller_shop_service,
                        database
                    ))

    # 셀러샵 카테고리 조회 엔드포인트
    app.add_url_rule('/shops/<int:seller_id>/category',
                     view_func=SellerShopCategoryView.as_view(
                         'seller_shop_category_view',
                         seller_shop_service,
                         database
                     ))

    # 셀러샵 상품 조회 엔드포인트
    app.add_url_rule('/shops/<int:seller_id>/products',
                     view_func=SellerShopProductListView.as_view(
                         'seller_shop_product_list_view',
                         seller_shop_service,
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

    app.add_url_rule('/event/products/category',
                     view_func=EventProductsCategoryView.as_view(
                         'event_product_category_view',
                         services.event_service,
                         database
                     ))

    app.add_url_rule('/event/products',
                     view_func=EventProductsToAddView.as_view(
                         'event_product_to_add_view',
                         services.event_service,
                         database
                     ))

# ----------------------------------------------------------------------------------------------------------------------
# 김민서 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------

    app.add_url_rule('/admin/orders',
                     view_func=OrderView.as_view(
                        'order_view',
                         order_service,
                         database
                     ))

    app.add_url_rule('/admin/orders',
                     view_func=OrderView.as_view(
                         'order_update_status_view',
                         order_service,
                         database
                     ))

    app.add_url_rule('/admin/orders/detail/<int:order_item_id>',
                     view_func=OrderDetailView.as_view(
                         'order_detail_view',
                         order_detail_service,
                         database
                     ))

    app.add_url_rule('/admin/orders/detail',
                     view_func=OrderDetailView.as_view(
                         'order_detail_update_view',
                         order_detail_service,
                         database
                     ))

    app.add_url_rule('/admin/orders/excel',
                     view_func=OrderExcelView.as_view(
                         'order_excel_view',
                         order_excel_service,
                         database
                     ))


# ----------------------------------------------------------------------------------------------------------------------
# 이성보 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# 이성보 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------
    app.add_url_rule('/enquiries',
                     view_func=EnquiryView.as_view(
                         'enquiry_view',
                         services.enquiry_service,
                         database
                     ))

    app.add_url_rule('/answer/<int:enquiry_id>',
                     view_func=AnswerView.as_view(
                         'answer_view',
                         services.enquiry_service,
                         database
                     ))
# ----------------------------------------------------------------------------------------------------------------------
# Admin 2 Section
# ----------------------------------------------------------------------------------------------------------------------
# 김영환 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------
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
    app.add_url_rule('/admin/search',
                     view_func=SellerSearchView.as_view(
                         'seller_search_view',
                         seller_service,
                         database
                     ))
    app.add_url_rule('/admin/sellers',
                     view_func=SellerListView.as_view(
                         'seller_list_view',
                         seller_service,
                         database
                     ))

# ----------------------------------------------------------------------------------------------------------------------
# 심원두 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------
    app.add_url_rule('/admin/product/productRegist/main_category',
                     view_func=MainCategoriesListView.as_view(
                         'main_category_list_view',
                         product_create_service,
                         database
                     ))
    
    app.add_url_rule('/admin/product/productRegist',
                     view_func=CreateProductView.as_view(
                         'product_create_view',
                         product_create_service,
                         database
                     ))
    
    app.add_url_rule('/admin/products',
                     view_func=ProductManageSearchView.as_view(
                         'product_manage_search_view',
                         product_manage_service,
                         database
                     ))
    
    app.add_url_rule('/admin/products/<string:product_code>',
                     view_func=ProductManageDetailView.as_view(
                         'product_manage_detail_view',
                         product_manage_service,
                         database
                     ))

# ----------------------------------------------------------------------------------------------------------------------
# 이영주 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------
    app.add_url_rule('/admin/<int:account_id>',
                     view_func=SellerInfoView.as_view(
                         'SellerInfoView',
                         seller_info_service,
                         database
                     ))

    app.add_url_rule('/admin/<int:account_id>/history',
                     view_func=SellerHistoryView.as_view(
                         'SellerHistoryView',
                         seller_info_service,
                         database
                     ))

    app.add_url_rule('/admin/status',
                     view_func=SellerStatusView.as_view(
                         'SellerStatusView',
                         seller_info_service,
                         database
                     ))

    app.add_url_rule('/admin/<int:account_id>/change_password',
                     view_func=SellerPasswordView.as_view(
                         'SellerPasswordView',
                         seller_info_service,
                         database
                     ))

# ----------------------------------------------------------------------------------------------------------------------
# 장재원 ◟( ˘ ³˘)◞ ♡
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    # don't touch this
    error_handle(app)
# ----------------------------------------------------------------------------------------------------------------------
