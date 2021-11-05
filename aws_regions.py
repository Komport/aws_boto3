from typing import List
from aws_boto3 import Boto
class Regions(Boto): #Regions class inherits Boto class. As of now can return all regions.

    def __init__(self):
        super().__init__() #Initialize parent class

    def get_regions(self) -> List: #Returns list of all AWS regions
        b = self.get_boto_client()
        regions = b.describe_regions()
        all_regions = []
        for reg in regions['Regions']:
            all_regions.append(reg['RegionName'])
        return all_regions
