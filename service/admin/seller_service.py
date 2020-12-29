import requests
# from utils.custom_exceptions import


class SellerInfoService:
    def __init__(self, seller_dao):
        self.seller_dao = seller_dao

    def get_seller_Info_service(self, connection, request): # get인데 데이타를 받아야 하는지? 아니지않나? 리퀘스트아님? 장고에서
        try:
 #          seller_id = data['seller_id']
            seller_id = request.GET.get('seller_id')
            
