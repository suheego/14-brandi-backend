from utils.custom_exceptions import UserAlreadyExist


class EnquiryService:

    def __init__(self, enquiry_dao):
        self.enquiry_dao = enquiry_dao

    def get_enquiry_service(self, connection, data):

        try:
            return self.enquiry_dao.get_dao(connection, data)

        except KeyError:
            raise KeyError('key_error')
