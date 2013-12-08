import smtplib
from email.mime.text import MIMEText
import conf

def feedbackmail(to_address,mail_subject,mail_content):
    direct=conf.mail_dir + mail_content
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
