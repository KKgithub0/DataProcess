#!/usr/bin/env python
# encoding: gbk


import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import email
import sys
import commands

if len(sys.argv)<5:
    print "Usage:\n\tpython %s DATE RECEIVER ATTACHMENT(s)" % __file__
    exit(1)

title = u"日常统计-top1000"
if len(sys.argv)>5:
    title = sys.argv[5].decode('gbk') + '-' + title
root = commands.getstatusoutput('pwd')[1]
RECEIVER_IN = sys.argv[2]

sender = 'xuyikai@baidu.com'
receivers = []
#mail_msg = open(sys.argv[3],'rb').read()
# load receivers
if '.txt' in sys.argv[2]:
    receiver_file = open(sys.argv[2])
    for line in receiver_file.readlines():
        receivers.append(line.strip())
else:
    for each in sys.argv[2].split(';'):
        receivers.append(each)



message = MIMEMultipart('related')
message['From'] = Header("xuyikai@baidu.com"+'\n', 'gbk')
message['To'] =  Header('; '.join(receivers)+'\n', 'gbk')
subject = '%s-%s' % (title.encode('gbk'), sys.argv[1])
date = sys.argv[1]
message['Subject'] = Header(subject, 'gbk')
message.attach(MIMEText('日常top统计，详见附件！谢谢！', 'plain', 'gbk'))

fp=open(sys.argv[3],'rb')
subtype = sys.argv[3].split('.')[1]
att = email.mime.application.MIMEApplication(fp.read(), _subtype=subtype)
fp.close()
att.add_header('Content-Disposition','attachment',filename=('%s_%s.%s' % (u'top数据'.encode('utf8') , date, subtype) ))
message.attach(att)

fp=open(sys.argv[4],'rb')
#subtype = sys.argv[4].split('.')[1]
att = email.mime.application.MIMEApplication(fp.read(), _subtype=subtype)
fp.close()
att.add_header('Content-Disposition','attachment',filename=('%s_%s.%s' % (u'数据'.encode('utf8') , date, subtype) ))
message.attach(att)


# 添加附件
# attachment = MIMEText(attach_file, 'base64', 'gbk')
# attachment['Content-Type'] = 'application/octet-stream'
# attachment["Content-Disposition"] = 'attachment; filename="total_report_%s.csv"' % date
# message.attach(attachment)
# attachment3 = MIMEText(attach_file3, 'base64', 'gbk')
# attachment3['Content-Type'] = 'application/octet-stream'
# attachment3["Content-Disposition"] = 'attachment; filename="zhineng_report_%s.csv"' % date
# message.attach(attachment3)

try:
    smtpObj = smtplib.SMTP('mail1-in.baidu.com')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "邮件发送成功"
except smtplib.SMTPException:
    print "Error: 无法发送邮件"
