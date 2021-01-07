from model import ProductEnquiryDao


class ProductEnquiryService:
    """ Business Layer

        Attributes:
            product_enquiry_dao : ProductEnquiryDao 클래스

        Author: 김민구

        History:
            2020-01-04(김민구): 초기 생성
    """

    def __init__(self):
        self.product_enquiry_dao = ProductEnquiryDao()

    def product_enquiry_list_logic(self, connection, data):
        """ 상품 enquiry 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : view에서 넘겨 받은 dict (product_id, type, offset, limit, [user_id])
                    type = self, all

            Author: 김민구

            Returns: 상품에 대한 Q&A 리스트, 질문 유형 리스트를 반환
            {    "enquiries": [
                    {
                        "answer": {
                            "account_id": 2,
                            "content": "답변드릴게요",
                            "created_at": "2021-01-04 12:38:12",
                            "enquiry_id": 102,
                            "id": 52,
                            "seller_name": "나는셀러2"
                        },
                        "content": "임시질문인데요2(답변감사합니다)",
                        "created_at": "2021-01-04 11:31:26",
                        "enquiry_id": 102,
                        "enquiry_type_id": 1,
                        "enquiry_type_name": "상품 문의",
                        "is_completed": 1,
                        "is_secret": 0,
                        "product_id": 1,
                        "user_id": 152
                    }
                ],
                "enquiry_types": [
                    {
                        "id": 1,
                        "name": "상품 문의"
                    }
                ]
            }

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

            History:
                2021-01-04(김민구): 초기 생성
        """

        enquiry_types = self.product_enquiry_dao.get_enquiry_type_list(connection)

        enquiry_list = self.product_enquiry_dao.get_product_enquiry_list(connection, data)
        data['enquiry_ids'] = tuple(enquiry['id'] for enquiry in enquiry_list if enquiry['is_completed'] == 1)

        replies = {}
        if data['enquiry_ids']:
            replies = self.product_enquiry_dao.get_enquiry_reply_list(connection, data)

        enquiries = [{
            "enquiry_id": enquiry['id'],
            "product_id": enquiry['product_id'],
            'user_id': enquiry['user_id'],
            'content': enquiry['content'],
            'enquiry_type_id': enquiry['enquiry_type_id'],
            'enquiry_type_name': enquiry['enquiry_type_name'],
            'is_secret': enquiry['is_secret'],
            'created_at': enquiry['created_at'],
            'is_completed': enquiry['is_completed'],
            'answer': replies.get(enquiry['id'], {})
        } for enquiry in enquiry_list]

        return {'enquiries': enquiries, 'enquiry_types': enquiry_types}

    def my_page_enquiry_list_logic(self, connection, data):
        """ 해당 유저의 상품 enquiry 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                data       : view에서 넘겨 받은 dict (product_id, type, offset, limit, user_id)
                    type = wait, complete, all

            Author: 김민구

            Returns: 해당 유저의 Q&A 리스트를 반환
            {    "enquiries": [
                    {
                        "answer": {
                            "account_id": 2,
                            "content": "답변드릴게요",
                            "created_at": "2021-01-04 12:38:12",
                            "enquiry_id": 102,
                            "id": 52,
                            "seller_name": "나는셀러2"
                        },
                        "content": "임시질문인데요2(답변감사합니다)",
                        "created_at": "2021-01-04 11:31:26",
                        "enquiry_id": 102,
                        "enquiry_type_id": 1,
                        "enquiry_type_name": "상품 문의",
                        "is_completed": 1,
                        "is_secret": 0,
                        "product_id": 1,
                        "user_id": 152
                    }
                ]
            }

            Raises:
                400, {'message': 'key_error', 'error_message': format(e)} : 잘못 입력된 키값

            History:
                2021-01-04(김민구): 초기 생성
        """

        enquiry_list = self.product_enquiry_dao.get_my_page_enquiry_list(connection, data)

        replies = {}
        if data['type'] != 'wait':
            data['enquiry_ids'] = tuple(enquiry['id'] for enquiry in enquiry_list if enquiry['is_completed'] == 1)
            if data['enquiry_ids']:
                replies = self.product_enquiry_dao.get_enquiry_reply_list(connection, data)

        enquiries = [{
            "enquiry_id": enquiry['id'],
            "product_id": enquiry['product_id'],
            'user_id': enquiry['user_id'],
            'content': enquiry['content'],
            'enquiry_type_id': enquiry['enquiry_type_id'],
            'enquiry_type_name': enquiry['enquiry_type_name'],
            'is_secret': enquiry['is_secret'],
            'created_at': enquiry['created_at'],
            'is_completed': enquiry['is_completed'],
            'answer': replies.get(enquiry['id'], {})
        } for enquiry in enquiry_list]

        return {'enquiries': enquiries}
