import smtplib
import requests
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
ami_name='pranav-snapshot-test_bkp_2017-02-13_12-51-07'

def send_mail():
	fromaddr = "pranav.bhardwaj@imaginea.com"
	toaddr = "pranavbhardwaj91@gmail.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "AMI Generated Successfully for "+ ami_name 
 
	body = """AMI Generated Successfully






        ***Please do not reply to this email; this address is not monitored***"""

	msg.attach(MIMEText(body, 'plain'))
 	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "Maruti@2017")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	return "Success in sending email..."

send_mail()