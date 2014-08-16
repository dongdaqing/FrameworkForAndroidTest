# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import loggingmodule
import os, smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class SendEmail(object):
    def __init__(self,filename):
        self.MAIL_TO_LIST = ["dongdaqing@youku.com"]
        self.MAIL_CC_LIST = ["dongdaqing@youku.com"]
        self.MAIL_HOST = "mail.youku.com"
        self.MAIL_USER = "username"
        self.MAIL_PASS = "password"
        self.MAIL_POSTFIX = "youku.com"
        self.MAIL_FROM = self.MAIL_USER + "<"+self.MAIL_USER + "@" + self.MAIL_POSTFIX + ">"

        self.logger = loggingmodule.Logger('sendemail',filename)
        self.root_path = os.path.dirname(filename)

        #用户测试文件路径
        self.file_path = '/Users/dongdaqing/temp/filelist'

    def send_mail(self, subject, content, filename = None):
        try:
            message = MIMEMultipart()
            message.attach(MIMEText(content))
            message["Subject"] = subject
            message["From"] = self.MAIL_FROM
            message["To"] = ";".join(self.MAIL_TO_LIST)
            message["Cc"] = ";".join(self.MAIL_CC_LIST)

            for file in filename:
                ctype, encoding = mimetypes.guess_type(file)
                if ctype is None or encoding is not None:
                    ctype = "application/octet-stream"
                maintype, subtype = ctype.split("/", 1)
                attachment = MIMEImage((lambda f: (f.read(), f.close()))(open(file, "rb"))[0], _subtype = subtype)
                attachment.add_header("Content-Disposition", "attachment", filename = os.path.basename(file))
                message.attach(attachment)

            smtp = smtplib.SMTP()
            smtp.connect(self.MAIL_HOST)
            smtp.login(self.MAIL_USER, self.MAIL_PASS)
            smtp.sendmail(self.MAIL_FROM, self.MAIL_TO_LIST+self.MAIL_CC_LIST, message.as_string())
            smtp.quit()

            return True
        except Exception, errmsg:
            print "Send mail failed to: %s" % errmsg
        return False

    def begintosend(self):
        os.chdir(self.root_path)
        cur_filelist = os.listdir('.')
        if self.send_mail("测试信", "测试邮件正文", cur_filelist):
#            print "发送成功！"
            self.logger.log("邮件发送成功")
        else:
#            print "发送失败！"
            self.logger.log("邮件发送失败")


if __name__ == "__main__":

    sendmail_obj = SendEmail()
    sendmail_obj.begintosend()
