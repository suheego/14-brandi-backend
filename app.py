from flask import Flask
from flask_cors import CORS

from model import SampleUserDao, UserDao, DestinationDao, CartItemDao
from service import SampleUserService, UserService, DestinationService, CartItemService
from view import create_endpoints


# for getting multiple service classes
class Services:
    pass


def create_app(test_config=None):
    app = Flask(__name__)
    app.debug = True

    # By default, submission of cookies across domains is disabled due to the security implications.
    CORS(app, resources={r'*': {'origins': '*'}})

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = app.config['DB']

    # persistence Layers
    sample_user_dao = SampleUserDao()
    user_dao = UserDao()
    destination_dao = DestinationDao()
    cart_item_dao = CartItemDao()

    # business Layer,   깔끔한 관리 방법을 생각하기
    services = Services
    services.sample_user_service = SampleUserService(sample_user_dao)
    services.user_service = UserService(user_dao, app.config)
    services.destination_service = DestinationService(destination_dao)
    services.cart_item_service = CartItemService(cart_item_dao)

    # presentation Layer
    create_endpoints(app, services, database)

    return app
