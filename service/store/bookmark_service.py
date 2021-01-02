from model import BookmarkDao
from utils.custom_exceptions import AlreadyExistBookmark, NotExistBookmark


class BookmarkService:
    """ Business Layer

        Attributes:
            bookmark_dao : BookmarkDao 클래스

        Author: 김민구

        History:
            2020-01-02(김민구): 초기 생성
    """

    def __init__(self):
        self.bookmark_dao = BookmarkDao()

    def post_bookmark_logic(self, connection, data):
        """ 상품 북마크 추가

        Args:
            connection: 데이터베이스 연결 객체
            data: view에서 넘겨 받은 dict( product_id, account_id )

        Returns:
            None

        Raises:
            400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

        History:
            2021-01-02(김민구): 초기 생성
        """

        exist = self.bookmark_dao.get_bookmark_exist(connection, data)
        if exist:
            raise AlreadyExistBookmark('이미 추가된 북마크입니다.')

        self.bookmark_dao.create_bookmark(connection, data)

        data['count'] = 1
        self.bookmark_dao.update_bookmark_volume_count(connection, data)

    def delete_bookmark_logic(self, connection, data):
        """ 상품 북마크 삭제

        Args:
            connection: 데이터베이스 연결 객체
            data: view에서 넘겨 받은 dict( product_id, account_id )

        Returns:
            None

        Raises:
            400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

        History:
            2021-01-02(김민구): 초기 생성
        """

        exist = self.bookmark_dao.get_bookmark_exist(connection, data)
        if not exist:
            raise NotExistBookmark('해당 북마크가 존재하지 않습니다.')

        self.bookmark_dao.delete_bookmark(connection, data)

        data['count'] = -1
        self.bookmark_dao.update_bookmark_volume_count(connection, data)
