import decimal

from flask.json import JSONEncoder
from flask import Flask
from flask_cors import CORS

from view import create_endpoints

#admin
from model import OrderDao
from model import SellerDao
from model import CreateProductDao

from service import OrderService
from service import SellerService
from service import CreateProductService
from service import EventService

#service
from model import (
    SampleUserDao,
    DestinationDao,
    CartItemDao,
    SenderDao,
    EventDao,
    ProductListDao,
    StoreOrderDao,
    SellerShopDao
)

from service import (
    SampleUserService,
    UserService,
    DestinationService,
    CartItemService,
    SenderService,
    EventService,
    ProductListService,
    StoreOrderService,
    CategoryListService,
    SellerShopService,
    BookmarkService,
    EventListService,
    ProductEnquiryService
)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        import datetime, decimal
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat(sep=' ')
            if isinstance(obj, datetime.datetime):
                return obj.isoformat(sep=' ')
            if isinstance(obj, decimal.Decimal):
                return float(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


# for getting multiple service classes
class Services:
    pass


def create_app(test_config=None):
    app = Flask(__name__)
    app.debug = True
    app.json_encoder = CustomJSONEncoder
    # By default, submission of cookies across domains is disabled due to the security implications.
    CORS(app, resources={r'*': {'origins': '*'}})

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = app.config['DB']
    secret_key = app.config['SECRET_KEY']

    # persistence Layers
    sample_user_dao = SampleUserDao()
    destination_dao = DestinationDao()
    cart_item_dao = CartItemDao()
    sender_dao = SenderDao()
    event_dao = EventDao()
    store_order_dao = StoreOrderDao()
    order_dao = OrderDao()
    seller_dao = SellerDao()
    create_product_dao = CreateProductDao()


    seller_shop_dao = SellerShopDao()

    # business Layer,   깔끔한 관리 방법을 생각하기
    services = Services
    services.sample_user_service = SampleUserService(sample_user_dao)
    services.user_service = UserService(app.config)
    services.destination_service = DestinationService(destination_dao)
    services.cart_item_service = CartItemService(cart_item_dao)
    services.store_order_service = StoreOrderService(store_order_dao)
    services.product_list_service = ProductListService()
    services.category_list_service = CategoryListService()
    services.event_list_service = EventListService()
    services.sender_service = SenderService(sender_dao)
    services.event_service = EventService(event_dao)
    services.order_service = OrderService(order_dao)
    services.seller_service = SellerService(seller_dao, app.config)
    services.create_product_service = CreateProductService(create_product_dao)
    services.bookmark_service = BookmarkService()
    services.product_enquiry_list_service = ProductEnquiryService()

    services.seller_shop_service = SellerShopService(seller_shop_dao)
    
    # presentation Layer
    create_endpoints(app, services, database)

    return app
