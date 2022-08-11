#!/usr/bin/python
# Filename: ami_backup_config.py

# example of config file
# time in minutes AMI images will be kept for
backup_retention =  10080 #7 days
# file to save the script logs
logfile = "/tmp/AMIBackup.txt"
# servers to be backed up
servers = [
    dict(
        name = "pranav-snapshot-test", #server description
        profile = "default", #account authentication profile name as set in the boto config file
        region = "ap-south-1", #ec2 server region
        pattern = "pranav-snapshot-test" #name tag of the server to backup
    ),
    dict(
        name = "pranav-webserver-az-1a",
        profile = "default",
        region = "ap-south-1",
        pattern = "pranav-webserver-az-1a"
    )
]
