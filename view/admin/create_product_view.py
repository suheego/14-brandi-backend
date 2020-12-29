import flask
from flask import jsonify, request
from flask.views import MethodView

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import RequiredFiledRule, NumberRule, GenderRule, AlphabeticRule
from flask_request_validator import (
    Param,
    JSON,
    validate_params,
    FORM
)
# from service.admin.create_product_service import CreateProductService

class CreateProductView(MethodView):
    
    def __init__(self, service, database):
        self.service = service
        self.database = database
    
    @validate_params(
        Param('seller_id',              FORM, str,  required=True),
        Param('account_id',             FORM, str,  required=True),
        Param('is_sale',                FORM, bool, required=True),
        Param('is_display',             FORM, bool, required=True),
        Param('main_category_id',       FORM, int,  required=True),
        Param('sub_category_id',        FORM, int,  required=True),
        Param('is_product_notice',      FORM, bool, required=True),
        Param('manufacturer',           FORM, str,  required=False),
        Param('manufacturing_date',     FORM, str,  required=False),
        Param('product_origin_type_id', FORM, str,  required=False),
        Param('product_name',           FORM, str,  required=True),
        Param('description',            FORM, str,  required=True),
        Param('detail_information',     FORM, str,  required=True),
        Param('options',                FORM, list, required=True),
        Param('minimum_quantity',       FORM, str,  required=False),
        Param('maximum_quantity',       FORM, str,  required=False),
        Param('origin_price',           FORM, str,  required=True),
        Param('discount_rate',          FORM, str,  required=True),
        Param('discounted_price',       FORM, str,  required=True),
        Param('discount_start_date',    FORM, str,  required=False),
        Param('discount_end_date',      FORM, str,  required=False)
    )
    def post(self, *args):
        data = {
            'seller_id'              : request.form.get('seller_id'),
            'account_id'             : request.form.get('account_id'),
            'is_sale'                : request.form.get('is_sale'),
            'is_display'             : request.form.get('is_display'),
            'main_category_id'       : request.form.get('main_category_id'),
            'sub_category_id'        : request.form.get('sub_category_id'),
            'is_product_notice'      : request.form.get('is_product_notice'),
            'manufacturer'           : request.form.get('manufacturer', None),
            'manufacturing_date'     : request.form.get('manufacturing_date', None),
            'product_origin_type_id' : request.form.get('product_origin_type_id', None),
            'product_name'           : request.form.get('product_name'),
            'description'            : request.form.get('description'),
            'detail_information'     : request.form.get('detail_information'),
            'options'                : request.form.get('options'),
            'minimum_quantity'       : request.form.get('minimum_quantity'),
            'maximum_quantity'       : request.form.get('maximum_quantity'),
            'origin_price'           : request.form.get('origin_price'),
            'discount_rate'          : request.form.get('discount_rate'),
            'discounted_price'       : request.form.get('discounted_price'),
            'discount_start_date'    : request.form.get('discount_start_date', None),
            'discount_end_date'      : request.form.get('discount_end_date', None),
        }

        product_images = flask.request.files.getlist("imageFiles")
        
        try:
            connection = get_connection(self.database)
            
            # products 테이블 insert
            last_row_id = self.service.create_product(connection, data)
            
            # products 테이블 update (product_code)
            self.service.update_product_code(connection, last_row_id)
            
            # product_images 테이블 insert
            self.service.create_product(connection, product_images)
            
            connection.commit()

            return {'message': 'success'}
            # return jsonify({'message': 'success'}, 200)
        
        except Exception as e:
            connection.rollback()
            raise e
        
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')