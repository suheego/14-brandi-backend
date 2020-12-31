from flask         import Flask
from flask_cors    import CORS

from model         import SampleUserDao
from model.admin   import SellerInfoDao, SellerDao, CreateProductDao

from service       import SampleUserService
from service.admin import SellerInfoService, SellerService, CreateProductService

from view.admin    import create_endpoints
from view          import create_endpoints

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
    sample_user_dao    = SampleUserDao()
    seller_dao         = SellerInfoDao()
    seller_dao         = SellerDao()
    create_product_dao = CreateProductDao()

    # business Layer
    services = Services
    services.seller_service         = SellerInfoService(seller_dao)
    services.seller_service         = SellerService(seller_dao, app.config)
    services.sample_user_service    = SampleUserService(sample_user_dao)
    services.create_product_service = CreateProductService(create_product_dao)

    # presentation Layer
    create_endpoints(app, services, database)

    return app
