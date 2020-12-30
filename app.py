from flask import Flask
from flask_cors import CORS

from model.admin import SellerDao
from service.admin import SellerService
from model import SampleUserDao

from model.admin.create_product_dao import CreateProductDao
from service import SampleUserService
from service.admin.create_product_service import CreateProductService
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
    secret_key = app.config['SECRET_KEY']

    # persistence Layer
    sample_user_dao = SampleUserDao()
    seller_dao = SellerDao()
    create_product_dao = CreateProductDao()

    # business Layer
    services = Services

    services.seller_service = SellerService(seller_dao,app.config)
    services.sample_user_service = SampleUserService(sample_user_dao)
    services.create_product_service = CreateProductService(create_product_dao)

    # presentation Layer
    create_endpoints(app, services, database)

    return app


