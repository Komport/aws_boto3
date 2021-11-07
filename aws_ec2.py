from typing import List
from aws_regions import Regions
import logging
import botocore

#Logger for logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class ManageEc2(Regions):           #Class to manage EC2 instances

    def __init__(self):             #Initialize super class
        super().__init__() 

    def get_instances(self):
        """ 
        Description: 
            Returns list of AWS EC2 instance info only for the active region. 

        Args:
            Format: {"Reservations": ...}
                    Document with all instance information, ID, state, IP and so on
        """
        try:
            bc = self.get_boto_client()
            response = bc.describe_instances()
        except Exception as e:
            raise "Error fetching instance data!"
        return response

    def get_stopped_instances(self) -> List:
        """ 
        Description: 
            Returns list of AWS EC2 instance InstanceID only in stopped state for the active region. 

        Args:
            Format: [InstanceIDs,...]
                    InstanceID = ID of AWS EC2 instance
        """
        response = self.get_instances()
        logger.info('Instance info retrived.')
        ec2_info = response['Reservations']
        instance_ids = []
        for item in ec2_info:
            if item['Instances'][0]['State']['Code'] == 80:
                instance_ids.append(item['Instances'][0]['InstanceId'])
        return instance_ids
    
    def get_running_instances(self) -> List:
        """ 
        Description: 
            Returns list of AWS EC2 instance InstanceID only in running state for the active region. 

        Args:
            Format: [InstanceIDs,...]
                    InstanceID = ID of AWS EC2 instance
        """
        try:
            response = self.get_instances()
            logger.info('Instance info retrived.')
        except botocore.exceptions.ClientError as error:
            logger.error(error)
        finally:
            if not response:
                response = {"Reservations":""}
        ec2_info = response['Reservations']
        if ec2_info == "":
            raise "Looks like we have problem."
        instance_ids = []
        for item in ec2_info:
            if item['Instances'][0]['State']['Code'] == 16:
                instance_ids.append(item['Instances'][0]['InstanceId'])
        return instance_ids


    def get_instance_ids(self):
        """ 
        Description: 
            Returns list of AWS EC2 instance InstanceID for the active region. 

        Args:
            Format: [InstanceIDs,...]
                    InstanceID = ID of AWS EC2 instance
        """
        response = self.get_instances()
        
        instance_info = response['Reservations']
        instance_ids = []
        for item in instance_info:
            instance_ids.append(item['Instances'][0]['InstanceId'])
        return instance_ids

    def get_all_instances(self):
        """ 
        Description: 
            Returns all AWS EC2 instances InstanceID value. 

        Returns:
            Format: {'region':[InstanceIDs,...]} 
                region = AWS region for each instance
                InstanceID = ID of AWS EC2 instance
        """
        regions = self.get_regions()
        all_instances = {}
        for region in regions:
            self.set_region(region)
            try:
                instances = self.get_instance_ids()
            except botocore.exceptions.ClientError as error:
                logger.error(error)
            finally:
                pass
            if len(instances) > 0:
                all_instances[region] = []
                for ins in instances:
                    all_instances[region].append(ins)
            else:
                pass
        return all_instances
    
    def stop_instances(self, instance_ids):     
        """ 
        Description: 
            Stops all provided instances. 

        Args:
            Format: {'region':[InstanceIDs,...]} 
                region = AWS region for each instance
                InstanceID = ID of AWS EC2 instance
        """
        for region,instance in instance_ids.items():
            self.set_region(region)
            b = self.get_boto_client()
            b.stop_instances(InstanceIds=instance,DryRun=False)

    def start_instances(self, instance_ids):
        """ 
        Description: 
            Starts all provided instances. 

        Args:
            Format: {'region':[InstanceIDs,...]} 
                region = AWS region for each instance
                InstanceID = ID of AWS EC2 instance
        """
        for region,instance in instance_ids.items():
            self.set_region(region)
            b = self.get_boto_client()
            b.start_instances(InstanceIds=instance,DryRun=False)

    


