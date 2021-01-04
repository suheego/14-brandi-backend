from model import CategoryListDao


class CategoryListService:
    """ Business Layer

        Attributes:
            category_list_dao : CategoryListDao 클래스

        Author: 김민구

        History:
            2020-12-30(김민구): 초기 생성
            2020-12-31(김민구): category_list_dao를 import 해서 사용하는 방법으로 수정
    """

    def __init__(self):
        self.category_list_dao = CategoryListDao()

    def category_list_logic(self, connection):
        """ 3가지 카테고리 조회

            Args:
                connection : 데이터베이스 연결 객체

            Author: 김민구

            Returns: menus, main_categories, sub_categories를 반환
                {
                    'menus': [
                        {
                            'id' : 1,
                            'name' : '브랜드'
                            'main_categories': [
                                {
                                    'id' : 1,
                                    'name' : '상의',
                                    'menu_id' : 6
                                    'sub_categories': [
                                        {
                                            'id' : 1,
                                            'name' : '반팔티셔츠',
                                            'main_categories' : 1
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): docs 수정
        """

        first_category_list = self.category_list_dao.get_first_category_list(connection)
        second_category_list = self.category_list_dao.get_second_category_list(connection)
        third_category_list = self.category_list_dao.get_third_category_list(connection)
        result = [
            {
                'id': first['id'],
                'name': first['name'],
                'main_categories': [
                    {
                        'id': second['id'],
                        'name': second['name'],
                        'menu_id': second['menu_id'],
                        'sub_categories': [
                            {
                                'id': third['id'],
                                'name': third['name'],
                                'main_category_id': third['main_category_id']
                            } for third in third_category_list if third['main_category_id'] == second['id']
                        ]
                    } for second in second_category_list if second['menu_id'] == first['id']
                ]
            } for first in first_category_list]

        return result
