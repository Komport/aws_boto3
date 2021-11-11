from typing import List
from aws_regions import Regions
import logging
import botocore

#Logger for logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class ManageS3(Regions):           #Class to manage S3 Buckets

    def __init__(self):             #Initialize super class
        super().__init__() 
        self.set_service('s3')

    def get_buckets(self):
        bc = self.get_boto_client()
        response = bc.list_buckets()
        return response