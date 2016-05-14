# -*- coding:utf-8 -*-  
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
 
 
class Mail:
 
    def __init__(self, smtp, user, pwd):
        self.smtp = smtp
        self.user = user
        self.pwd = pwd
        self.isauth = True
 
    def parse_send(self, subject, content, plugin):
        return subject, content, plugin
 
    def send(self,  cclist=[], plugins=[]):
        s = smtplib.SMTP(self.smtp)
        s.set_debuglevel(smtplib.SMTP.debuglevel)
        if self.isauth:
            s.docmd("EHLO %s" % self.smtp)
 
        try:
            s.starttls()
        except smtplib.SMTPException, e:
            pass  # smtp 服务器不支持 ssl
 
        try:
	    try:	
                s.login(self.user, self.pwd)
		login_msg = "OK"
	    except:
		login_msg = "ERROR"
        except smtplib.SMTPException, e:
            pass  # smtp 服务器不需要登陆
 
        s.close()
        return login_msg
 
if __name__ == "__main__":
    mail = Mail('smtp.exmail.qq.com', 'x@163.com', 'xxxxxx')
    print  mail.send()
