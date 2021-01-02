
class ProductManageService:
    """ Business Layer

        Attributes:
            product_manage_dao : ProductManageDao 클래스

        Author: 심원두

        History:
            2020-12-31(심원두): 초기 생성
    """
    
    def __init__(self, product_manage_dao):
        self.product_manage_dao = product_manage_dao
        
    def search_product_service(self, connection, data):
        """ product 검색
        
            Parameters:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 dict 객체
            
            Author: 심원두

            Returns:
                -
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)} : 잘못 입력된 키값
        """
        try:
            print("service")
            return self.product_manage_dao.search_products(connection, data)
            
        except KeyError:
            raise KeyError('key_error')