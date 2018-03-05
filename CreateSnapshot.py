import json
import urllib.parse


import boto3
from datetime import datetime,timedelta

print('Loading function')

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
	instances = ec2.instances.filter(Filters=[{'Name': 'tag:AutoBackup', 'Values': ['yes',]}]).all()
	for instance in instances:
		print("Find AutoSnapshot tagged intance:", instance.id) 
		for volume in instance.volumes.all():
			print("Create snapshot for volume: "+volume.id)
			ec2.create_snapshot(VolumeId=volume.id, Description=instance.private_dns_name+" "+volume.id)