class EnquiryService:

    def __init__(self, enquiry_dao):
        self.enquiry_dao = enquiry_dao

    def get_enquiry_service(self, connection, data):
        try:
            data['page'] = (data['page'] - 1) * data['length']
            if data['product_name']:
                data['product_name'] = '%' + data['product_name'] + '%'
            if data['seller_name']:
                data['seller_name'] = '%' + data['seller_name'] + '%'
            return self.enquiry_dao.get_enquiries_list(connection, data)

        except Exception as e:
            raise e
