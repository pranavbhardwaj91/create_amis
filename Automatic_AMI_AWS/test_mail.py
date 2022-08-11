import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import requests


def send_mail():

	fromaddr = 'pranav.bhardwaj@imaginea.com'
	toaddrs = ['pranavbhardwaj91@gmail.com']
	msg = """AMIBackup Script
    Subject: AMIBackup Script successfully created AMI

        AMIBackup Script successfully created AMI







        ***Please do not reply to this email; this address is not monitored***
        """
	username = 'pranav.bhardwaj@imaginea.com'
	password = 'Maruti@2017'
	#server = smtplib.SMTP('smtp.gmail.com',587)
	server = smtplib.SMTP_SSL('smtp.gmail.com:465')
        server.ehlo()
	server.starttls()
        try:
	    server.login(username, password)
        except Exception as e:
            print str(e) + ":  " + e.message
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
	return "Success in sending email..."




send_mail()

