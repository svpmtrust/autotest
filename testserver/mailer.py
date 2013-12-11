import smtplib
from email.mime.text import MIMEText
import conf
import time

email_addresses={}

def load_address():
    fi=open(conf.mail_dir + 'user_list.csv')    
    for user_email in fi:
        user_email=user_email.strip()
        username,email=user_email.split(',')
        email_addresses[username]=email


def feedbackmail(to_user,mail_subject,content):
    user_list=email_addresses[to_user]
    msg=MIMEText(content)
    
    msg['Subject']=mail_subject
    msg['From']= 'testvebsmail@gmail.com'
    msg['to']= user_list
    
    s=smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login('testvebsmail@gmail.com','Vebsnet2')
    s.sendmail('testvebsmail@gmail.com', [user_list], msg.as_string())
    s.quit()
    time.sleep(5)
