#!/usr/bin/python
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
current_datetime = datetime.datetime.now()
servers = ami_backup_config.servers
backup_retention = ami_backup_config.backup_retention

#import pdb; pdb.set_trace()
for server in servers:
    server_name = server['name']
    account_profile = server['profile']
    server_pattern = server['pattern']
    server_region = server['region']
    conn = boto.ec2.connect_to_region(server_region,profile_name=account_profile)
    images = conn.get_all_images(filters = {'tag:Name':server_pattern + signature + '*'})



    print "Deletion of old AMIs"
    
    for image in images:
    	
    	image_name=image.tags['Name']
    	print "image_name " +  image_name
    	
    	image_id = image.id
    	print "image_id " + image_id
    	
    	image_stamp = image_name.replace(server_pattern + signature, "")
    	print "image_stamp " + image_stamp
    	
    	image_timestamp = mktime(time.strptime(image_stamp, "%Y-%m-%d_%H-%M-%S"))
    	print "image_timestamp "+ str(image_timestamp)
    	
    	current_timestamp = mktime(current_datetime.timetuple())
    	print "current_timestamp " + str(current_timestamp)
    	
    	diff_minutes = (current_timestamp - image_timestamp) / 60
    	print "diff_minutes " + str(diff_minutes)
	
