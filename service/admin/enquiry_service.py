from utils.custom_exceptions import EnquiryFilterNotExist, DateMissingOne, EventSearchTwoInput


class EnquiryService:
    """ Business Layer

            Attributes:
                enquiry_dao: EnquiryDao 클래스

            Author: 이성보

            History:
                2020-12-28(이성보): 초기 생성
                2020-12-29(이성보): q&a 리스트 조회 서비스 생성
                2020-12-30(이성보): q&a 디테일 조회 서비스 생성
    """
    def __init__(self, enquiry_dao):
        self.enquiry_dao = enquiry_dao

    def get_enquiry_service(self, connection, data):
        """ GET 메소드: 이벤트 리스트 조회

            Args:
                connection: 데이터베이스 연결 객체
                data      : View 에서 넘겨받은 dict

            Author: 이성보

            Returns:
                {
                    "enquiries": [
                        {
                            "answer": "답변입니다50",
                            "answer_date": "2020-12-28 13:31:58",
                            "answer_user": "seller8",
                            "enquiry_type": "상품 문의",
                            "id": 100,
                            "is_answered": "답변",
                            "is_secret": "비공개",
                            "membership_number": 151,
                            "phone_number": "01099990151",
                            "product_name": "성보의하루1",
                            "question": "질문이 있습니다(답변감사합니다)50",
                            "registration_date": "2020-12-28 13:31:58",
                            "seller_name": "나는셀러9"
                        },
                        {
                            "answer": "답변입니다49",
                            "answer_date": "2020-12-28 13:31:58",
                            "answer_user": "seller8",
                            "enquiry_type": "상품 문의",
                            "id": 99,
                            "is_answered": "답변",
                            "is_secret": "비공개",
                            "membership_number": 150,
                            "phone_number": "01099990150",
                            "product_name": "성보의하루1",
                            "question": "질문이 있습니다(답변감사합니다)49",
                            "registration_date": "2020-12-28 13:31:58",
                            "seller_name": "나는셀러9"
                        }
                    ],
                    "total_count": 2
                }

            Raises:
                400, {'message': 'key error',
                'errorMessage': 'key_error'} : 잘못 입력된 키값

            History:
                2020-12-28(이성보): 초기 생성
                2020-12-29(이성보): 검색 조건에 맞게 변형로직 작성
        """
        try:
            data['page'] = (data['page'] - 1) * data['length']

            if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
                raise DateMissingOne('start_date or end_date is missing')

            if data['product_name'] and data['seller_name']:
                raise EventSearchTwoInput('search value accept only one of name or number')

            if data['product_name']:
                data['product_name'] = '%' + data['product_name'] + '%'

            return self.enquiry_dao.get_enquiries_list(connection, data)

        except Exception as e:
            raise e
