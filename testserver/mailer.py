import smtplib
from email.mime.text import MIMEText
import conf
import time

email_addresses={}

def load_address():
    fi=open(conf.mail_dir + 'to_address.csv')    
    for user_email in fi:
        user_email=user_email.strip()
        username,email=user_email.split(',')
        email_addresses[username]=email


def feedbackmail(to_user,mail_subject,template_name):
    to_address=email_addresses[to_user]
    direct=conf.mail_dir + template_name
    fp=open(direct,'rb')
    msg=MIMEText(fp.read())
    fp.close()
    
    msg['Subject']=mail_subject
    msg['From']= 'testvebsmail@gmail.com'
    msg['to']= to_address
    
    s=smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login('testvebsmail@gmail.com','Vebsnet2')
    s.sendmail('testvebsmail@gmail.com', [to_address], msg.as_string())
    s.quit()
    time.sleep(5)
