from flask.json import JSONEncoder
from flask import Flask
from flask_cors import CORS

from model import SampleUserDao, UserDao, DestinationDao, CartItemDao, SenderDao, EventDao, ProductListDao, OrderDao
from service import SampleUserService, UserService, DestinationService, CartItemService, SenderService, EventService, ProductListService, OrderService
from view import create_endpoints

from model.admin import SellerDao
from model.admin.create_product_dao import CreateProductDao

from service.admin import SellerService
from service.admin.create_product_service import CreateProductService

from view import create_endpoints

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        import datetime
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat(sep=' ')
            if isinstance(obj, datetime.datetime):
                return obj.isoformat(sep=' ')
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


    user_dao = UserDao()
    destination_dao = DestinationDao()
    cart_item_dao = CartItemDao()
    order_dao = OrderDao()
    
    user_dao = UserDao()
    destination_dao = DestinationDao()
    cart_item_dao = CartItemDao()
    product_list_dao = ProductListDao()
    sender_dao = SenderDao()
    event_dao = EventDao()

    seller_dao = SellerDao()
    create_product_dao = CreateProductDao()

    # business Layer,   깔끔한 관리 방법을 생각하기
    services = Services
    services.sample_user_service = SampleUserService(sample_user_dao)

    services.user_service = UserService(user_dao, app.config)
    services.destination_service = DestinationService(destination_dao)
    services.cart_item_service = CartItemService(cart_item_dao)
    services.order_service = OrderService(order_dao)
    services.product_list_service = ProductListService(product_list_dao)
    services.sender_service = SenderService(sender_dao)
    services.event_service = EventService(event_dao)

    services.seller_service = SellerService(seller_dao,app.config)
    services.create_product_service = CreateProductService(create_product_dao)
    
    # presentation Layer
    create_endpoints(app, services, database)

    return app