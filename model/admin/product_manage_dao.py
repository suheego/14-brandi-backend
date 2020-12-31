import pymysql

class ProductManageDao:
    """ Persistence Layer

        Attributes: None

        Author: 심원두

        History:
            2020-12-31(심원두): 초기 생성
    """
    
    def search_products(self, connection, data):
        """상품 정보 검색
        
        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받은 상품 검색에 사용될 키값

        Author: 심원두
        
        Returns: [{}]

        History:
            2020-12-31(심원두): 초기 생성
        
        Raises:
            500, {'message': '-',
                  'errorMessage': '-'} : --
        """
        
        sql = """
            SELECT
                ~
            FROM
                products
            ;
        """
        
        print(sql)
        result = "--"
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # cursor.execute(sql)
            # result = cursor.fetchall()
    
            # if not result:
            #     raise --('--')
    
            return result