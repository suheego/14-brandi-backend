import boto3
from flask import current_app

class S3FileManager:
    """ Amazon S3 파일 업로드 클래스
        Attributes:
            s3  : boto3 를 통해서 생성된 Amazon S3 인스턴스

        Author: 심원두

        History:
            2020-12-31(심원두): 초기 작성
    """
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
            aws_secret_access_key=current_app.config['S3_SECRET_KEY']
        )

    def file_upload(self, file, file_name):
        """ Amazon S3 파일 업로드 클래스
            Args:
                filefunc  : View 에서 받은 이미지 파일
                file_name : 해당 파일명

            Author: 심원두

            Returns:
                file_name : 인자로 받은 파일명. 정상 처리 되었을 경우 해당 파일명을 다시 반환

            History:
                2020-20-31(심원두): 초기 생성
        """
        self.s3.upload_fileobj(
            file,
            current_app.config['S3_BUCKET_NAME'],
            file_name
        )
        return file_name


class GenerateFilePath:
    """ 파일 이미지 저장 경로 생성
        Args:
            path_type :
                1: 셀러 프로필 이미지를 저장 경로 생성 명시
                2: 셀러 배경 이미지 저장 경로 생성 명시
                3: 상품 이미지 저장 경로 명시
                4: 기획전 베너 이미지 저장 경로 명시
                5: 기획전 상세 이미지 저장 경로 명시

            **kwargs : 저장 경로 생성에 이용될 seller_id 혹은 product_id

        Author: 심원두

        Returns: 이미지 파일 저장 경로

        History:
            2020-12-31(심원두): 초기 생성
            2021-01-02(강두연): 이벤트 관련 경로 추가
    """
    def generate_file_path(self, path_type, **kwargs):
        # TODO
        event_path = 'events/'

        seller_path = 'sellers/'

        if path_type is 1:
            return seller_path + + str(kwargs['seller_id']) + '/profile/'

        if path_type is 2:
            return seller_path + str(kwargs['seller_id']) + '/background/'

        if path_type is 3:
            return seller_path + str(kwargs['seller_id']) + '/products/' + str(kwargs['product_id']) + '/images/'

        if path_type is 4:
            return event_path + str(kwargs['today']) + '/banners/'

        if path_type is 5:
            return event_path + str(kwargs['today']) + '/details/'
