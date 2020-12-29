class CreateProductService:
    
    def __init__(self, create_product_dao):
        self.create_product_dao = create_product_dao
        
    def create_product(self, connection, data):
        try:
            seller_id              = data['seller_id']
            account_id             = data['account_id']
            is_sale                = data['is_sale']
            is_display             = data['is_display']
            main_category_id       = data['main_category_id']
            sub_category_id        = data['sub_category_id']
            is_product_notice      = data['is_product_notice']
            manufacturer           = data['manufacturer']
            manufacturing_date     = data['manufacturing_date']
            product_origin_type_id = data['product_origin_type_id']
            product_name           = data['product_name']
            description            = data['description']
            detail_information     = data['detail_information']
            options                = data['options']
            minimum_quantity       = data['minimum_quantity']
            maximum_quantity       = data['maximum_quantity']
            origin_price           = data['origin_price']
            discount_rate          = data['discount_rate']
            discounted_price       = data['discounted_price']
            discount_start_date    = data['discount_start_date']
            discount_end_date      = data['discount_end_date']
            
            # is_product_notice 가 True 일 때 하위 항목 필수 입력 처리
            if is_product_notice:
                if not manufacturer or not manufacturing_date or not product_origin_type_id:
                    # 예외처리
                    pass
            
            # 최소 판매량, 최대 판매량 비교 예외처리
            if minimum_quantity > maximum_quantity:
                # 예외처리
                pass
            
            # 세일율이 0 아 아닌 경우, 하위 항목 필수 입력 처리
            if float(discount_rate) is not 0:
                if not discount_start_date or not discount_end_date:
                    # 예외처리
                    pass
                
                print(discount_start_date)
                print(discount_end_date)
                
                # 세일 시작 날짜, 세일 종료 날짜 비교 예외처리
                if discount_start_date > discount_end_date:
                    # 예외처리
                    pass
            
            # products 테이블 insert dao 호출
            return self.create_product_dao.insert_product(connection, data)
        
        except KeyError:
            raise KeyError('key_error')
    
    def update_product_code(self, connection, last_row_id):
        data = dict()
        
        # 상품 코드 생성
        data['product_code'] = 'P' + str(last_row_id).zfill(18)
        data['product_id']   = last_row_id
        
        return self.create_product_dao.update_product_code(connection, data)
    
    def create_product_images(self, connection, data):
        try:
            seller_id = data['image_url']
            account_id = data['product_id']
            is_sale = data['order_index']
            
            # for image in images:
            #     # TODO : 대표이미지 필수 항목 체크
            #
            #     # TODO : check file size(4mb 이상 예외처리)
            #     print(len(image.read()))
            #
            #     # TODO : check image type(only jpg)
            #     print(image.content_type)
            #
            #     # TODO : check image size(640, 720)
        
        except KeyError:
            raise KeyError('key_error')