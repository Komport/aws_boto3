from aws_regions import Regions

class ManageEc2(Regions):           #Class to manage EC2 instances

    def __init__(self):             #Initialize super class
        super().__init__() 

    def get_instances(self):        #Returns EC2 instance all information in default region
        try:
            bc = self.get_boto_client()
            response = bc.describe_instances()
        except Exception as e:
            raise "Error fetching instance data!"
        return response

    def get_stopped_instances(self) -> str:     #Returns only stopped EC2 instances
        response = self.get_instances()
        ec2_info = response['Reservations']
        instance_ids = []
        for item in ec2_info:
            if item['Instances'][0]['State']['Code'] == 80:
                instance_ids.append(item['Instances'][0]['InstanceId'])
        return instance_ids
    
    def get_running_instances(self) -> str:     #Returns instances only in running state
        response = self.get_instances()
        ec2_info = response['Reservations']
        instance_ids = []
        for item in ec2_info:
            if item['Instances'][0]['State']['Code'] == 16:
                instance_ids.append(item['Instances'][0]['InstanceId'])
        return instance_ids


    def get_instance_ids(self):                 #Returns EC2 instance IDs in the default region
        response = self.get_instances()
        
        instance_info = response['Reservations']
        instance_ids = []
        for item in instance_info:
            instance_ids.append(item['Instances'][0]['InstanceId'])
        return instance_ids

    def get_all_instances(self):                #Returns EC2 instance IDs in all regions
        regions = self.get_regions()
        all_instances = {}
        for region in regions:
            self.set_region(region)
            instances = self.get_instance_ids()
            if len(instances) > 0:
                all_instances[region] = []
                for ins in instances:
                    all_instances[region].append(ins)
            else:
                pass
        return all_instances
    
    def stop_instances(self, instance_ids):     #Stops all provided instances. Accepts {'region':[InstanceIDs,...]}
        for region,instance in instance_ids.items():
            print(region,instance)
            self.set_region(region)
            b = self.get_boto_client()
            b.stop_instances(InstanceIds=instance,DryRun=False)

    def start_instances(self, instance_ids):    #Starts all provided instances. Accepts {'region':[InstanceIDs,...]}
        for region,instance in instance_ids.items():
            print(region,instance)
            self.set_region(region)
            b = self.get_boto_client()
            b.start_instances(InstanceIds=instance,DryRun=False)

