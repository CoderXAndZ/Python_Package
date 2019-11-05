#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 上传到 fir.im PostToFirIm.py

import os
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
from tkinter import messagebox


# 将ipa包上传到fir_im
# ipa_path:ipa包路径,
# emails:邮件地址,多个地址英文逗号分隔
# update_description:更新内容
def post_to_fir_im(ipa_path, emails, update_description):
    # 登录 fir.im  token 44f0de5d6180e642acb59c592c567ca9
    result = os.popen('fir login -T 1adcc557a27afaf0341816186905cd5c').read()
    print('登录fir.im结果：\n', result)
    if 'succeed' in result:
        print('================= 登录fir.im成功 =================')
    else:
        print('================= 登录fir.im失败 =================')

    # # 发布 ipa 到 fir.im
    print('================= 开始发布ipa包到 fir.im =================')
    # -r 获取当前版本的24位 release_id
    pulish_result = os.popen('fir publish %s -c %s -Q' % (ipa_path, update_description)).read()
    # pulish_result = os.popen('fir publish %s' % ipa_path).read()
    print('发布 ipa结果：\n', pulish_result)
    if 'succeed' in pulish_result:
        print('================= 发布成功 =================')
        split = (pulish_result.split('\n')[7])
        load_url = "https://fir.im/2jyf?release_id=" + split[-24:]  # ipa包 下载地址
        print(split, '\n 下载地址:', load_url)

        # print("\n\n", pulish_result.split('\n')[7][-24:], "\n\n")

        send_email(load_url, emails)
    else:
        print('================= 发布失败 =================')

    # # 蒲公英上传
    # 执行 curl -F "file=@/tmp/example.ipa" -F "uKey=xxx" -F "_api_key=xxx" https://qiniu-storage.pgyer.com/apiv1/app/upload 请根据开发者自己的账号，将其中的 uKey 和 _api_key 的值替换为相应的值。


# 发送邮件给测试人员
def send_email(url, emails):
    # 输入Email地址和口令:
    from_addr = '928186296@qq.com'  # input('From: ')
    password = 'efumhglhenstbbhi'  # input('Password: ')
    # 输入收件人地址: 接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可。
    # to_addr = '1935722630@qq.com, 351812401@qq.com'  # input('To: ')
    to_addr = emails
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'  # input('SMTP server: ')

    content = '最新的安装包可以下载了，地址是：\n %s \n请在Safari中打开链接进行下载，如果遇到"未受信任开发者的的情况"，请到 "设置-通用-设备管理" 中添加信任即可，祝测试愉快！😁' % url
    message = MIMEText(content, 'plain', 'utf-8')  # 第一个参数就是邮件正文，第二个参数是MIME的subtype，传入'plain'表示纯文本
    message['From'] = _format_addr('开发人员徐雪 <%s>' % from_addr)
    message['To'] = _format_addr('测试组人员 <%s>' % to_addr)
    message['Subject'] = Header('来自开发人员的问候……', 'utf-8').encode()

    # 加密 SMTP
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)  # SMTP协议默认端口是25
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr.split(','), message.as_string())
    server.quit()
    messagebox.showinfo("温馨提示", "打包完毕！")


# 格式化一个邮件地址，注意不能简单地传入name <addr@example.com>，因为如果包含中文，需要通过Header对象进行编码。
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
    # 我们必须把From、To和Subject添加到MIMEText中，才是一封完整的邮件


# if __name__ == '__main__':
    # archive_project(input('输入开机密码，授权访问钥匙串：\n'))
    # emails = input("请输入测试人员邮箱,多个邮箱请使用英文逗号隔开：")

    # post_to_fir_im( ,'1935722630@qq.com', "adhoc包")
    # post_to_fir_im('http://fir.im/el4t', '1935722630@qq.com')
    # post_ipa()

    # send_email('http://fir.im/el4t ')