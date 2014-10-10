import smtplib
from email.mime.text import MIMEText
import conf
import time
import os

email_addresses={}

def load_address():
    fi=open(conf.mail_dir + 'user_list.csv')    
    for user_email in fi:
        user_email=user_email.strip()
        if not user_email:
            continue
        username,dummy,email=user_email.split(',')
        email_addresses[username]=email

from_addr = 'VEBSNET2-NO-REPLY <do.not.reply@aviso.com>'

def feedbackmail(to_user,mail_subject,content):
    user_list=email_addresses[to_user]
    msg=MIMEText(content)
    
    
    msg['Subject']=mail_subject
    msg['From']= from_addr
    msg['to']= user_list
    
    s=smtplib.SMTP(os.environ['MAIL_HOST'])
    s.ehlo()
    s.starttls()
    s.login(os.environ['MAIL_USER'],os.environ['MAIL_PWD'])
    s.sendmail(from_addr, [user_list], msg.as_string())
    s.quit()
    time.sleep(5)
