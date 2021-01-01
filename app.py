import decimal

from flask.json    import JSONEncoder
from flask         import Flask
from flask_cors    import CORS

from view import create_endpoints

#admin
from model   import OrderDao
from service import OrderService

#admin2
from model   import SellerInfoDao, SellerDao, ProductCreateDao, ProductManageDao
from service import SellerService, SellerInfoService, ProductCreateService, ProductManageService

#service
from model import (
    SampleUserDao,
    UserDao,
    DestinationDao,
    CartItemDao,
    SenderDao,
    EventDao,
    ProductListDao,
    StoreOrderDao
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
    CategoryListService
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

    # persistence Layer
    sample_user_dao    = SampleUserDao()
    destination_dao    = DestinationDao()
    cart_item_dao      = CartItemDao()
    sender_dao         = SenderDao()
    event_dao          = EventDao()
    store_order_dao    = StoreOrderDao()
    order_dao          = OrderDao()
    
    # admin2
    seller_dao         = SellerDao()
    seller_info_dao    = SellerInfoDao()
    product_create_dao = ProductCreateDao()
    product_manage_dao = ProductManageDao()
    
    # business Layer,   깔끔한 관리 방법을 생각하기
    # service
    services = Services
    services.sample_user_service   = SampleUserService(sample_user_dao)
    services.user_service          = UserService(app.config)
    services.destination_service   = DestinationService(destination_dao)
    services.cart_item_service     = CartItemService(cart_item_dao)
    services.store_order_service   = StoreOrderService(store_order_dao)
    services.product_list_service  = ProductListService()
    services.category_list_service = CategoryListService()
    services.sender_service        = SenderService(sender_dao)
    
    #admin1
    services.event_service = EventService(event_dao)
    services.order_service = OrderService(order_dao)
    
    #admin2
    services.seller_service         = SellerService(seller_dao, app.config)
    services.seller_info_service    = SellerInfoService(seller_info_dao)
    services.product_create_service = ProductCreateService(product_create_dao)
    services.product_manage_service = ProductManageService(product_manage_dao)

    # presentation Layer
    create_endpoints(app, services, database)
    
    return app