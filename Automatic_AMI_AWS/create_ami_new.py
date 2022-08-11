#!/usr/bin/python
#This script will generate AMI of the instances mentioned in ami_backup_config.
#Kindly add the email in fromaddr and toaddr before using this script.
#It will send email notification on succesfull creation of AMI.


import boto
import boto.ec2
import time
import os
import sys
import logging
import datetime
import smtplib
import ami_backup_config
from time import mktime
import smtplib
import requests
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

logger = logging.getLogger('AMIBackup')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(lineno)d - %(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(ami_backup_config.logfile)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
signature = "_bkp_"

#Function defined for sending mail after sucessfull creation of AMI
def send_mail_success():
	fromaddr = "<Mention the Email here>"
	toaddr = "<Mention the Email here>"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "AMI Generated Successfully for "+ ami_name 
 
	body = """AMI Generated Successfully






        ***Please do not reply to this email; this address is not monitored***"""

	msg.attach(MIMEText(body, 'plain'))
 	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "<Mention the password of email account mentioned in fromaddr>")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	return "Success in sending email..."

def send_mail_fail():
	fromaddr = "<Mention the Email here>"
	toaddr = "<Mention the Email here>"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "AMI Generated Failed for "+ ami_name 
 
	body = """AMI Generation Failed. Please check in AWS Console Manually.






        ***Please do not reply to this email; this address is not monitored***"""

	msg.attach(MIMEText(body, 'plain'))
 	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "<Mention the password of email account mentioned in fromaddr>")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	return "Success in sending email..."


#Reading servers from ami_backup_config file
servers = ami_backup_config.servers
backup_retention = ami_backup_config.backup_retention




print "Connecting to EC2..."
#Adding the server details to various variables

for server in servers :
    server_name = server['name']
    account_profile = server['profile']
    server_pattern = server['pattern']
    server_region = server['region']
    conn = boto.ec2.connect_to_region(server_region,profile_name=account_profile)
    
    if ( conn is None ):
    	print "ERROR - " + server_name + ": unable to connect"
    	logger.error(server_name + ": unable to connect to region " + server_region + " with profile " + account_profile)
    	
    print "Starting the AMI creation of "+ server_name+" mentioned in ami_backup_config.py file..."
    reservations = conn.get_all_instances(filters = {'tag:Name':server_pattern, 'instance-state-name':'*'})
    if ( len(reservations) == 0 ):
    	print "ERROR - " + server_name + ": unable to find server " + server_pattern
    	logger.error( server_name + ": unable to find server " + server_pattern )
    	
    for reservation in reservations:
    	for instance in reservation.instances:
    		instance_name = instance.tags['Name']
    		instance_id = instance.id
    		print server_name + ": " + instance_id +" will be backedup "+ instance_name
    		current_datetime = datetime.datetime.now()
    		date_stamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    		ami_name = instance_name +signature + date_stamp
    		try:
    			print "Starting for instance: " + instance_name
    			ami_id=instance.create_image(ami_name,description="Created by AMI Backup Script",no_reboot=True,dry_run=False)
    			print "AMI id is: " + ami_id
    			logger.info("AMI of " + instance_name +" "+" with instanceid: "+instance_id +" having ami name as: " + ami_name + " with ami_id as: "+ ami_id+ " is created")
    			imgs=conn.get_image(ami_id)
    			while imgs.state == 'pending':
    				time.sleep(5)
    				imgs.update()
    				if imgs.state == 'available':
    					print "Tagging the ami created: "+ ami_id
    					imgs.add_tag("Name", ami_name)
    					send_mail_success()
    					logger.info("Tagging of " + instance_name + ": " + ami_name + " having ami_id as: "+ ami_id+ " is created")
    				else:
    					logger.info("Waiting for ami of " + instance_name + ": " + ami_name + " having ami_id as: "+ ami_id+" to become available")
    					
    		except Exception, e:
    			send_mail_fail()
    			logger.error("Backup of " + instance_name + ": " + ami_name + " having ami_id as: "+ ami_id+ " is failed " + e.message)
    			exit()
    		time.sleep(10)
    		continue

#import pdb; pdb.set_trace()
print "\n Deletion of 7 Days old AMI and its corresponding snapshots"
for server in servers:
	server_name = server['name']
	account_profile = server['profile']
	server_pattern = server['pattern']
	server_region = server['region']
	conn = boto.ec2.connect_to_region(server_region,profile_name=account_profile)
	images = conn.get_all_images(filters = {'tag:Name':server_pattern + signature + '*'})
	for image in images:
		image_name=image.tags['Name']
		image_id = image.id
		image_stamp = image_name.replace(server_pattern + signature, "")
		image_timestamp = mktime(time.strptime(image_stamp, "%Y-%m-%d_%H-%M-%S"))
		current_timestamp = mktime(current_datetime.timetuple())
		diff_minutes = (current_timestamp - image_timestamp) / 60
		if ( diff_minutes > backup_retention ):
			image.deregister(delete_snapshot=True, dry_run=False)
			print image_name + " deleted"
			logger.info("Deleted AMI " + image_name )
		else:
			print image_name + " kept"
			logger.info("Kept AMI " + image_name )
logger.info("Backup Completed")
print "\nBackup Completed"














