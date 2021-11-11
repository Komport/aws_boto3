from typing import List
import boto3

class Boto: #Boto3 initializing class
    __client = None

    def __init__(self,region="us-east-2",service="ec2"): #Initialize class with default region
        self.__region = region
        self.__service = service

    def get_boto_client(self): #Return boto3 client object
        self.__client = boto3.client(self.__service,region_name=self.__region)
        return self.__client

    def set_region(self,region): #Set default region
        self.__region = region

    def set_service(self,service): #Set default aws service
        self.__service = service