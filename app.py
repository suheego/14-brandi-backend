from flask import Flask
from flask_cors import CORS


from model import SampleUserDao, OrderDao, EventDao
from service import SampleUserService, OrderService, EventService

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

    # persistence Layer
    sample_user_dao = SampleUserDao()
    order_dao = OrderDao()
    event_dao = EventDao()

    # business Layer
    services = Services
    services.sample_user_service = SampleUserService(sample_user_dao)
    services.order_service = OrderService(order_dao)
    services.event_service = EventService(event_dao)



    # presentation Layer
    create_endpoints(app, services, database)

    return app
