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
			print("Find Volume:" ,volume.id)
			snapshots = ec2.snapshots.filter(Filters=[{'Name': 'volume-id', 'Values': [volume.id]}]).all()
			for snapshot in snapshots:
				if (datetime.utcnow()-snapshot.start_time.replace(tzinfo=None))>timedelta(minutes=30):
					print ("find old snapshot and delete: ", snapshot.id)
					snapshot.delete()
				else:
					print ("newer snapshot: ", snapshot.id) 