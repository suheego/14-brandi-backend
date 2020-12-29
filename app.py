from flask import Flask
from flask_cors import CORS

from model.admin import SellerInfoDao
from service.admin import SellerInfoService
from view.admin import create_endpoints

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
    seller_dao = SellerInfoDao()

    # business Layer
    services = Services
    services.seller_service = SellerInfoService(seller_dao)

    # presentation Layer
    create_endpoints(app, services, database)

    return app
