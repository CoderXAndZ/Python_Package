# -*- coding: utf-8 -*-
import re
import requests
import filecmp
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from bs4 import BeautifulSoup
import sys

from email.parser import Parser
from email.message import Message
from email.message import EmailMessage
from email.header import decode_header
from email.utils import parseaddr
import poplib

#
# import poplib
# import email
# from email.parser import Parser
# from email.header import decode_header
# from email.utils import parseaddr
#
# def decode_str(s):
#     value, charset = decode_header(s)[0]
#     if charset:
#         value = value.decode(charset)
#     return value
#
#
# def guess_charset(msg):
#     # 先从msg对象获取编码:
#     charset = msg.get_charset()
#     if charset is None:
#         # 如果获取不到，再从Content-Type字段获取:
#         content_type = msg.get('Content-Type', '').lower()
#         pos = content_type.find('charset=')
#         if pos >= 0:
#             charset = content_type[pos + 8:].strip()
#     return charset
#
#
# def get_email_headers(msg):
#     # 邮件的From, To, Subject存在于根对象上:
#     headers = {}
#     for header in ['From', 'To', 'Subject', 'Date']:
#         value = msg.get(header, '')
#         if value:
#             if header == 'Date':
#                 headers['date'] = value
#             if header == 'Subject':
#                 # 需要解码Subject字符串:
#                 subject = decode_str(value)
#                 headers['subject'] = subject
#             else:
#                 # 需要解码Email地址:
#                 hdr, addr = parseaddr(value)
#                 name = decode_str(hdr)
#                 value = u'%s <%s>' % (name, addr)
#                 if header == 'From':
#                     from_address = value
#                     headers['from'] = from_address
#                 else:
#                     to_address = value
#                     headers['to'] = to_address
#     content_type = msg.get_content_type()
#     print('head content_type: ', content_type)
#     return headers
#
#
# # indent用于缩进显示:
# def get_email_cntent(message, base_save_path):
#     j = 0
#     content = ''
#     attachment_files = []
#     for part in message.walk():
#         j = j + 1
#         file_name = part.get_filename()
#         contentType = part.get_content_type()
#         # 保存附件
#         if file_name:  # Attachment
#             # Decode filename
#             h = email.Header.Header(file_name)
#             dh = email.Header.decode_header(h)
#             filename = dh[0][0]
#             if dh[0][1]:  # 如果包含编码的格式，则按照该格式解码
#                 print("------------------- [0][1]:", dh[0][1], '', "--------：", filename, "---------")
#                 # filename = unicode(filename, dh[0][1])
#                 # filename = filename.encode("utf-8")
#             data = part.get_payload(decode=True)
#             att_file = open(base_save_path + filename, 'wb')
#             attachment_files.append(filename)
#             att_file.write(data)
#             att_file.close()
#         elif contentType == 'text/plain' or contentType == 'text/html':
#             # 保存正文
#             data = part.get_payload(decode=True)
#             charset = guess_charset(part)
#             if charset:
#                 charset = charset.strip().split(';')[0]
#                 print('charset:', charset)
#                 data = data.decode(charset)
#             content = data
#     return content, attachment_files
#
#
# if __name__ == '__main__':
#     # 输入邮件地址, 口令和POP3服务器地址:
#     emailaddress = '3199597553@qq.com'
#     # 注意使用开通POP，SMTP等的授权码
#     password = 'omyxftohabcpdhdh'
#     pop3_server = 'pop.qq.com'
#
#     # 连接到POP3服务器:
#     server = poplib.POP3(pop3_server)
#     # 可以打开或关闭调试信息:
#     # server.set_debuglevel(1)
#     # POP3服务器的欢迎文字:
#     print(server.getwelcome())
#     # 身份认证:
#     server.user(emailaddress)
#     server.pass_(password)
#     # stat()返回邮件数量和占用空间:
#     messagesCount, messagesSize = server.stat()
#     print('messagesCount:', messagesCount)
#     print('messagesSize:', messagesSize)
#     # list()返回所有邮件的编号:
#     resp, mails, octets = server.list()
#     print('------ resp ------')
#     print(resp)  # +OK 46 964346 响应的状态 邮件数量 邮件占用的空间大小
#     print('------ mails ------')
#     print(mails)  # 所有邮件的编号及大小的编号list，['1 2211', '2 29908', ...]
#     print('------ octets ------')
#     print(octets)
#
#     # 获取最新一封邮件, 注意索引号从1开始:
#     length = len(mails)
#     for i in range(length):
#         resp, lines, octets = server.retr(i + 1)
#         # lines存储了邮件的原始文本的每一行,
#         # 可以获得整个邮件的原始文本:
#         lines_b = str(lines[i])
#         msg_content = " ".join(lines_b)
#         # 把邮件内容解析为Message对象：
#         msg = Parser().parsestr(msg_content)
#
#         # 但是这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，
#         # 嵌套可能还不止一层。所以我们要递归地打印出Message对象的层次结构：
#         print('---------- 解析之后 ----------')
#         base_save_path = '/media/markliu/Entertainment/email_attachments/'
#         msg_headers = get_email_headers(msg)
#         content, attachment_files = get_email_cntent(msg, base_save_path)
#
#         print("--------------msg_headers:", msg_headers)
#
#         # print('subject:', msg_headers['Subject'])
#         # print('from_address:', msg_headers['From'])
#         # print('to_address:', msg_headers['To'])
#         # print('date:', msg_headers['Date'])
#         print('content:', content)
#         print('attachment_files: ', attachment_files)
#
#     # 关闭连接:
#     server.quit()

#####################################################################
#
# #!/usr/bin/python
# import imaplib
# import email
#
# mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
# mail.login('3199597553@qq.com', 'omyxftohabcpdhdh')
# mail.list()
# mail.select()
# typ, data = mail.search(None, 'UNSEEN')
# print("------------------", data)

############################################################3

# 输入邮件地址, 口令和POP3服务器地址:
email = '840772463@qq.com'   # 840772463@qq.com   3199597553@qq.com
password = 'axwidrunrmqlbfaa'  # 这个密码不是邮箱登录密码，是pop3服务密码：axwidrunrmqlbfaa   omyxftohabcpdhdh
pop3_server = 'pop.qq.com'


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject', 'Date']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    # print("-------------- value:", value, "--------------")
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, value)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%s part %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        has_send = 0
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('\033[1;34;35m %s Text: %s \033[0m' % ('  ' * indent, content + '...'))

        else:
            print('\033[7;32;43m %s Attachment: %s \033[0m' % ('  ' * indent, content_type))


if __name__ == '__main__':
    # 连接到POP3服务器:
    server = poplib.POP3_SSL(pop3_server, 995)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    # 身份认证:
    server.user(email)
    server.pass_(password)
    # stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    print(mails)

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    print('未读邮件的数量', index)

    for i in range(index - 7, index):  # 打印最新的7封邮件，
        resp, lines, octets = server.retr(i)  # 获取最新邮件
        # print('-----------octets:', octets, '\n -----------resp:\n', server.retr(i))
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        print_info(msg)
    # # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(2)
    # 关闭连接:
    server.quit()


##############################3333###############################3

#
# # reload(sys)
# sys.setdefaultencoding('utf-8')
#
# header = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
#     'Referer': 'http://www.bing.com/',
# }
#
# requests.packages.urllib3.disable_warnings()
#
#
# def process(p):
#     url = 'http://www.apple.com/cn-k12/shop'  # 抓取的网页地址
#     r = requests.get(url, headers=header, timeout=12999, verify=False)
#     r.encoding = "utf-8"  # 抓取的网页编码
#
#     soup = BeautifulSoup(r.text, "lxml")
#     titles = soup.select('div#page')  # 抓取的内容标签
#     res = []
#     for title in titles[:min(5, len(titles))]:
#         res.append(' '.join(title.get_text().split()))
#     return res
#
#
# if __name__ == '__main__':
#     r = filecmp.cmp(r'old.txt', r'new.txt')
#     if (r == True):
#         print(':(还木有更新')
#     else:
#         # 第三方SMTP服务
#         mail_host = "smtp.exmail.qq.com"  # 设置服务器（此处为腾讯企业邮箱）
#         mail_user = "admin@itaowei.cn"  # 邮箱地址
#         mail_pass = "mimaxiezaizheli"  # 密码
#
#         sender = 'admin@itaowei.cn'
#         receivers = ['taowei86@163.com']  # 接收邮箱地址
#         # 3个参数：第1个为文本内容，第2个plain设置文本格式，第3个utf-8设置编码
#         message = MIMEText('苹果教育商店更新啦！', 'plain', 'utf-8')
#         message['From'] = Header("itaowei.cn", 'utf-8')
#         message['To'] = Header("更新啦！", 'utf-8')
#         subject = '苹果教育商店更新啦！'
#         message['Subject'] = Header(subject, 'utf-8')
#
#         try:
#             smtpObj = smtplib.SMTP()
#             smtpObj.connect(mail_host, 25)  # 25为SMTP端口号
#             smtpObj.login(mail_user, mail_pass)
#             smtpObj.sendmail(sender, receivers, message.as_string())
#             print("邮件发送成功XD")
#         except smtplib.SMTPException:
#             print("Error: 无法发送邮件T_T")