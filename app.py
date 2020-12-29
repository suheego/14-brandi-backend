from flask import Flask
from flask_cors import CORS

from model import SampleUserDao, EventDao
from service import SampleUserService, EventService
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
<<<<<<< HEAD
    user_dao = UserDao()
    destination_dao = DestinationDao()
    cart_item_dao = CartItemDao()
=======
    event_dao = EventDao()
>>>>>>> 374da8252600bfd0d7cadecdc297353ed4e1bd81

    # business Layer
    services = Services
    services.sample_user_service = SampleUserService(sample_user_dao)
<<<<<<< HEAD
    services.user_service = UserService(user_dao, app.config)
    services.destination_service = DestinationService(destination_dao)
    services.cart_item_service = CartItemService(cart_item_dao)
=======
    services.event_service = EventService(event_dao)
>>>>>>> 374da8252600bfd0d7cadecdc297353ed4e1bd81

    # presentation Layer
    create_endpoints(app, services, database)

    return app
