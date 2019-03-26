#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
#  融托优选自动打包上传fir.im并发邮件通知开发人员

import os
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib

PROJECT_NAME = 'RTYX'  # 'RMGJ'
CONFIGURATION = 'Debug'
SCHEME = 'RTYX'  # 'RMGJ'

PROJECT_PATH = '/Users/admin/XZ公司项目/RTYX'  # '/Users/mac/XZ公司项目/rmgj'
XCWORKSPACE_PATH = '/Users/admin/XZ公司项目/RTYX/RTYX.xcworkspace'  # '/Users/mac/XZ公司项目/rmgj/RMGJ.xcworkspace'
ExportOptionsPlistPath = '/Users/admin/Desktop/关于打包/融托优选/ExportOptions.plist'
EXPORT_PATH = '/Users/admin/Desktop/关于打包/融托优选'
archive_path = '%s/%s.xcarchive' % (EXPORT_PATH, SCHEME)  # .archive 包的导出路径
ipa_path = '/Users/admin/Desktop/关于打包/融托优选/%s.ipa' % SCHEME


# 开机密码和测试人员邮箱
def archive_project(password, emails):

    xcodebuild = '/usr/bin/xcodebuild'  # 终端输入 which xcodebuild 获取路径

    # clean
    print("================= Clean =================")
    clean_comand = '%s clean -workspace %s ' \
                   '-configuration %s ' \
                   '-scheme %s' % (xcodebuild, XCWORKSPACE_PATH, CONFIGURATION, SCHEME)
    os.system(clean_comand)

    # archive
    print("================= Archive =================")
    # CFBundleVersion=  -destination generic/platform=ios CODE_SIGN_IDENTITY
    archive_comand = '%s archive -workspace %s ' \
                     '-scheme %s ' \
                     '-configuration %s ' \
                     '-archivePath %s' % (xcodebuild, XCWORKSPACE_PATH, SCHEME, CONFIGURATION, archive_path)
    os.system(archive_comand)

    # 获取用户的家目录
    home_path = os.path.expanduser("~")

    # unlock Keychain
    security = '/usr/bin/security'  # 终端输入 which security 获取路径 -p 后面跟的是开机密码
    unlock_comand = '%s unlock-keychain -p %s %s/Library/Keychains/login.keychain' % (security, password, home_path)
    os.system(unlock_comand)

    # export ipa
    export_comand = '%s -exportArchive -archivePath %s ' \
                    '-exportPath %s ' \
                    '-exportOptionsPlist %s ' \
                    '-allowProvisioningUpdates' % (xcodebuild, archive_path, EXPORT_PATH, ExportOptionsPlistPath)
    result = os.system(export_comand)

    print('导出结果：', result)

    if result == 0:
        print('================= 打包成功 =================')

        post_to_fir_im(emails)
    else:
        print('================= 打包失败 =================')


# 将ipa包上传到fir_im
def post_to_fir_im(emails):
    plist_buddy = '/usr/libexec/PlistBuddy'
    app_info_plist_path = '%s/Products/Applications/%s.app' % (archive_path, SCHEME)
    os.system('cd %s' % app_info_plist_path)
    # Version
    os.system('%s -c "print CFBundleShortVersionString" %s/Info.plist' % (plist_buddy, app_info_plist_path))
    # Build
    os.system('%s -c "print CFBundleVersion" %s/Info.plist' % (plist_buddy, app_info_plist_path))
    # Bundle Identifier
    bundle_identifier_tmp = os.popen('%s -c "print CFBundleIdentifier" %s/Info.plist' % (plist_buddy, app_info_plist_path)).read()
    # 当前target的名字
    projec_name_tmp = os.popen('%s -c "print CFBundleExecutable" %s/Info.plist' % (plist_buddy, app_info_plist_path)).read()
    print(bundle_identifier_tmp, projec_name_tmp)
    # app的名字
    os.system('%s -c "print CFBundleDisplayName" %s/Info.plist' % (plist_buddy, app_info_plist_path))
    # return

    # 登录 fir.im  token 44f0de5d6180e642acb59c592c567ca9
    result = os.popen('fir login -T 44f0de5d6180e642acb59c592c567ca9').read()
    print('登录fir.im结果：\n', result)
    if 'succeed' in result:
        print('================= 登录fir.im成功 =================')
    else:
        print('================= 登录fir.im失败 =================')

    # 发布 ipa 到 fir.im
    print('================= 开始发布ipa包到 fir.im =================')
    pulish_result = os.popen('fir publish %s' % ipa_path).read()
    print('发布 ipa结果：\n', pulish_result)
    if 'succeed' in pulish_result:
        print('================= 发布成功 =================')
        split = (pulish_result.split('\n')[12])
        load_url = split[68:]  # ipa包 下载地址
        print(split, '\n 下载地址:', load_url)
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


# 格式化一个邮件地址，注意不能简单地传入name <addr@example.com>，因为如果包含中文，需要通过Header对象进行编码。
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
    # 我们必须把From、To和Subject添加到MIMEText中，才是一封完整的邮件


if __name__ == '__main__':
    # archive_project(input('输入开机密码，授权访问钥匙串：\n'))
    # emails = input("请输入测试人员邮箱,多个邮箱请使用英文逗号隔开：")

    post_to_fir_im('http://fir.im/el4t', '1935722630@qq.com')

    # send_email('http://fir.im/el4t ')