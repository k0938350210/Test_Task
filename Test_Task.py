from dateutil.parser import parse
import requests
import boto3
import datetime

ec2 = boto3.resource('ec2')
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
my_inst={'i-0683517dcef7e0f00':'http://a.tezterz.com/', 'i-09dd4a157e7685fed':'http://b.tezterz.com/', , 'i-0038d32548d912450':'http://c.tezterz.com/'}


for i in my_inst:
	# Try sending requests to all EC2 (TCP and HTTP)
	try:
		response = requests.get(my_inst[i], timeout=3)
		print(i + '=' + my_inst[i] + '    |   response = ' + str(response.status_code))
	except Exception:
	# Get Name EC2
		for tags in ec2.Instance(i).tags:
			if tags["Key"] == 'Name':
				instancename = tags["Value"]
	# Creating AMI of the stopped EC2
		try:
			ec2.Instance(i).create_image(
			Description=str(instancename) + '_' + str(current_date),
			DryRun=False,
			Name=str(instancename) + '_' + str(current_date),
			NoReboot=True
			)
			ec2.Instance(i).terminate()
		except Exception as err:
			print(err)
##########################################################
age = 7
def days_old(date):
	get_date_obj = parse(date)
	date_obj = get_date_obj.replace(tzinfo=None)
	diff = datetime.datetime.now() - date_obj
	return diff.days
ec2 = boto3.client('ec2')
amis = ec2.describe_images(Owners=['self'])
for ami in amis['Images']:
	create_date = ami['CreationDate']
	ami_id = ami['ImageId']
	day_old = days_old(create_date)
	if day_old > age:
	# deregister the AMI
		ec2.deregister_image(ImageId=ami_id)

##########################################################
	# Printing all instances, INCLUDING terminated, with highlighting their current state
ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
         for tags in ec2.Instance(instance.id).tags:
                if tags["Key"] == 'Name':
                        instancename = tags["Value"]
                        print instance.id, instance.instance_type, '\x1b[6;30;42m' + instance.state['Name'] + '\x1b[0m', instancename



