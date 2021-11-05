**What?**

Interface to manage AWS recources.

**How?**
```bash
(.boto) yusif@yusifpc:~/aws/aws_boto3$ python
Python 3.7.5 (default, Feb 23 2021, 13:22:40) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from aws_ec2 import ManageEc2
>>> m = ManageEc2()
>>> m.get_all_instances()
{'us-east-2': ['i-07ca1521b37974ebc'], 'us-west-1': ['i-08321f1d574fef391']}
```
