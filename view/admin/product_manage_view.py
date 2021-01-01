import json

from flask                   import jsonify, request
from flask.views             import MethodView

from utils.connection        import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules             import NumberRule

from flask_request_validator import (
    Param,
    FORM,
    GET,
    MaxLength,
    validate_params,
)


class SearchProductView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : MainCategoryListService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 심원두

        History:
            2020-12-31(심원두): 초기 작성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database
        
    def get(self, *args):
        """GET 메소드: 특정 조건에 해당하는 상품 리스트를 조회한다.
        
            Args: None
            
            Author: 심원두
            
            Returns:
                return {"message": "success", "result": [{}]}
            
            Raises:
                400, {'message': 'invalid_parameter', 'errorMessage': str(e)}: 잘못된 요청값

            History:
                2020-12-31(심원두): 초기생성
        """
        
        try:
            connection = get_connection(self.database)
            print("view")
            data = dict()
            
            self.service.search_product_service(connection, data)
            
            return jsonify({'message': 'success', 'result': data})

        except Exception as e:
            raise e

        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')