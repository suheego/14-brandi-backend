from unittest import mock, TestCase

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import create_app


class TestUser(TestCase):
    """ Test

        Target: store/user_view

        Author: 김민구

        History:
            2020-20-30(김민구): 초기 생성
    """

    def setUp(self):
        app = create_app()
        self.client = app.test_client()

    @mock.patch('view.store.user_view.id_token')
    def test_social_sign_in(self, mock_id_token):
        """ POST 메소드: 유저 구글 소셜 로그인

            Decorator: 가짜 구글 라이브러리 함수를 만들기 위한 mock.patch 데코레이터

            Args: 가짜 구글 라이브러리 함수

            Author: 김민구

            Return:
                True: response.status_code == 200 : 유저 로그인 성공 status_code
                True: b'token' in response.data   : 유저 로그인 성공 토큰 확인 여부

            History:
                2020-20-30(김민구): 초기 생성

            Notes:
                소셜 로그인 구조상 Integration Test를 하기 힘들기 때문에 간략하게 성공 케이스를 확인하는 용도로 작성

        """

        mock_id_token.verify_oauth2_token.return_value = {
             "email": "test_user@gmail.com"
        }
        response = self.client.post('/users/social-signin', headers={'Authorization': 'google_token'})
        assert response.status_code == 200
        assert b'token' in response.data
