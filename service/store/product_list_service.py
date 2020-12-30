class ProductListService:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def product_list_service(self, connection, data):
        """ 상품 리스트와 이벤트 배너 조회

            Args:
                data       : View 에서 넘겨받은 dict 객체
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                {'product_list': product_list, 'event_list': event_list}

            Raises:
                400, {'message': 'key_error', 'errorMessage': format(e)}         : 잘못 입력된 키값

            History:
                2020-12-30(김민구): 초기 생성

            Notes:
                product 20개당 event 배너 1개씩

                offset이 0 혹은 20의 배수일 때는 event 배너가 1개
                20의 배수가 아닐 때는 event 배너가 2개

                ex) offset 0,  limit = 30 : product 1번부터~30번 (20)
                        event 배너 1개(1), event_offset = 0, event_limit = 1

                    offset 30, limit = 30 : product 31번부터 60번 (40, 60)
                        event 배너 2개(2,3), event_offset = 1, event_limit = 2

                    offset 60, limit = 30 : product 61번부터 90번 (80)
                        event 배너 1개(4), event_offset = 3, event_limit = 1

                    offset 90, limit = 30 : product 91번부터 120번 (100, 120)
                        event 배너 2개(5,6), event_offset = 4, event_limit = 2

                ** 1번 **
                event_offset = offset // 20
                event_limit = 1
                if offset % 20:
                    event_limit = 2

                ** 2번 **
                event_offset = offset // 20
                event_limit = 1 if not offset % 20 else 2

                ** 3번 **
                event_offset = offset // 20
                if not offset % 20:
                    event_limit = 1
                else:
                    event_limit = 2
        """

        product_list = self.product_dao.get_product_list(connection, data)

        offset = data['offset']
        if offset % 20 and offset != 0:
            event_limit = 2
        else:
            event_limit = 1

        event_offset = offset // 20
        event_data = {
            'limit': event_limit,
            'offset': event_offset
        }
        event_list = self.product_dao.get_event_list(connection, event_data)
        return {'product_list': product_list, 'event_list': event_list}

    def category_list_service(self, connection):
        """ 3가지 카테고리 조회

            Args:
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns:
                {
                    'menus': first_category_list,
                    'main_categories': second_category_list,
                    'sub_categories': third_category_list
                }

            Raises:
                400, {'message': 'key_error', 'errorMessage': format(e)}         : 잘못 입력된 키값

            History:
                2020-12-30(김민구): 초기 생성
        """

        first_category_list = self.product_dao.get_first_category_list(connection)
        second_category_list = self.product_dao.get_second_category_list(connection)
        third_category_list = self.product_dao.get_third_category_list(connection)
        return {
            'menus': first_category_list,
            'main_categories': second_category_list,
            'sub_categories': third_category_list
        }
