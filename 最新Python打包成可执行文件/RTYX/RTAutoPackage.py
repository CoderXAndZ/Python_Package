#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 融托优选和融米小管家 自动打包

import os
import shutil
from plistlib import *
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib


# 开机密码和测试人员邮箱 configuration
def archive_project(project_path, configuration, password, method):
    # 获取用户的家目录
    home_path = os.path.expanduser("~")

    ipa_output_path = home_path + "/Desktop/RTYX ipa"  # ipa 包的输出路径
    if os.path.exists(ipa_output_path):
        shutil.rmtree(ipa_output_path)  # 删除文件夹和文件夹里面的内容
    # 创建
    os.makedirs(ipa_output_path)

    project_name = os.path.basename(project_path)   # 根据全路径获取文件名称
    scheme = project_name.split('.')[0]
    project_file = os.path.dirname(project_path)   # 根据全路径获取文件所在路径
    archive_path = '%s/%s.xcarchive' % (ipa_output_path, scheme)  # .archive 包的导出路径
    ipa_path = '%s/%s.ipa' % (ipa_output_path, scheme)
    export_options_plist_path = '%s/ExportOptions.plist' % ipa_output_path

    print("输出路径：", ipa_output_path)
    print("项目名称：", project_name)
    print("SCHEME：", scheme)
    print("archive_path:", archive_path)
    print("ipa_path:", ipa_path)
    print("ExportOptionsPlistPath:", export_options_plist_path, "CONFIGURATION:", configuration, "password:", password)

    # 创建 ExportOptions.plist 文件
    create_export_options_plist(method, export_options_plist_path)

    print("================= 修改 bundle indentifier =================")
    # 如果打企业版的包，修改 bundle indentifier
    if method == "enterprise":
        print("================= 修改成enterprise版本indentifier =================")
        change_bundle_identifier(project_file, scheme, "com.rtyx.RTYXEn")
    else:
        print("================= 修改成App Store/ad-hoc版本indentifier =================")
        change_bundle_identifier(project_file, scheme, "com.rtyx.RTYX")

    xcodebuild = '/usr/bin/xcodebuild'  # 终端输入 which xcodebuild 获取路径

    # clean
    print("================= Clean =================")
    clean_comand = '%s clean -workspace %s ' \
                   '-configuration %s ' \
                   '-scheme %s' % (xcodebuild, project_path, configuration, scheme)
    os.system(clean_comand)
    print("clean工程：", clean_comand)

    # archive
    print("================= Archive =================")
    # CFBundleVersion=  -destination generic/platform=ios CODE_SIGN_IDENTITY
    archive_comand = '%s archive -workspace %s ' \
                     '-scheme %s ' \
                     '-configuration %s ' \
                     '-archivePath %s' % (xcodebuild, project_path, scheme, configuration, archive_path)
    os.system(archive_comand)
    print("archive工程：", archive_comand)

    # 如果打企业版的包，替换掉描述文件
    if method == "enterprise":
        change_profile(archive_path, "RTYXEnterpriseProfile/embedded.mobileprovision")
    else:
        change_profile(archive_path, "RTYXAppStoreProfile/embedded.mobileprovision")

    # unlock Keychain
    security = '/usr/bin/security'  # 终端输入 which security 获取路径 -p 后面跟的是开机密码
    unlock_comand = '%s unlock-keychain -p %s %s/Library/Keychains/login.keychain' % (security, password, home_path)
    os.system(unlock_comand)
    print("解锁钥匙串：", unlock_comand)

    print("================= 正在导出... =================")
    # export ipa
    export_comand = '%s -exportArchive -archivePath %s ' \
                    '-exportPath %s ' \
                    '-exportOptionsPlist %s ' \
                    '-allowProvisioningUpdates' % (xcodebuild, archive_path, ipa_output_path, export_options_plist_path)
    result = os.system(export_comand)
    print("导出工程：", export_comand)

    print('导出结果：', result)

    if result == 0:
        print('================= 打包成功 =================')

    else:
        print('================= 打包失败 =================')


# 创建 ExportOptions.plist 文件
def create_export_options_plist(method, plist_path):
    print("method：", method)

    if method == 'ad-hoc':  # ad-hoc包
        root_dict = {"compileBitcode": True,
                     "method": "ad-hoc",
                     "signingStyle": "automatic",
                     "stripSwiftSymbols": True,
                     "teamID": "8SD6K7E3YB",
                     "thinning": "<none>"}
        with open(plist_path, "wb+") as fp:
            dump(root_dict, fp)
    elif method == 'enterprise':  # 企业版
        root_dict = {"compileBitcode": True,
                     "destination": "export",
                     "method": "enterprise",
                     "signingStyle": "automatic",
                     "stripSwiftSymbols": True,
                     "teamID": "HKYG7W22CW",
                     "thinning": "<none>"}
        with open(plist_path, "wb+") as fp:
            dump(root_dict, fp)
    else:   # App Store版本导出
        root_dict = {
                     "destination": "export",
                     "method": "app-store",
                     "signingStyle": "automatic",
                     "stripSwiftSymbols": True,
                     "teamID": "8SD6K7E3YB",
                     "uploadBitcode": True,
                     "uploadSymbols": True
                    }
        with open(plist_path, "wb+") as fp:
            dump(root_dict, fp)


# 融托优选-企业版修改工程的 bundle identifier
def change_bundle_identifier(project_file, scheme, bundle_identifier):
    plist_buddy = '/usr/libexec/PlistBuddy'
    # /Users/admin/XZ公司项目/RTYX/RTYX/Info.plist
    app_info_plist_path = '%s/%s/Info.plist' % (project_file, scheme)
    # Set :CFBundleIdentifier com.rtyx.RTYXEn
    change_command = '%s -c "Set :CFBundleIdentifier %s"  %s' % (plist_buddy, bundle_identifier, app_info_plist_path)
    result = os.system(change_command)
    print("change_command:", change_command, "\n修改结果：", result)
    if result == 0:
        print("================= 修改 bundle indentifier 成功 =================")
    else:
        print("================= 修改 bundle indentifier 失败 =================")


# 融托优选- 替换 企业版/app-store、ad-hoc 描述文件
def change_profile(archive_path, profile_path):
    # 获取到融托优选的描述文件路径  RTYXEnterpriseProfile
    rtyx_profile = os.path.abspath(profile_path)
    # 目的路径
    destination_path = archive_path + "/Products/Applications/RTYX.app/embedded.mobileprovision"
    # 替换描述文件
    shutil.copy(rtyx_profile, destination_path)
    # /Users/admin/Library/Developer/Xcode/Archives/2019-02-14/RTYX 2019-2-14 下午3.23.xcarchive/Products/Applications/RTYX.app/embedded.mobileprovision
    # 当前目录 "/Users/admin/Documents/长久保存/Python打包/最新Python打包成可执行文件"
    # "/Users/admin/Documents/长久保存/Python打包/最新Python打包成可执行文件/RTYXEnterpriseProfile/embedded.mobileprovision"


# 自动打包 ---- 暂不使用
def auto_package(project_path ,SCHEME):
    # 获取用户的家目录
    homePath = os.path.expanduser("~")
    print("获取用户的家目录", homePath)
    finalPath = homePath + "/Desktop/RTYXipa"  # ipa 包的输出路径

    archive_path = '%s/%s.xcarchive' % (finalPath, SCHEME)  # .archive 包的导出路径

    ExportOptionsPlistPath = '%s/ExportOptions.plist' % finalPath

    plist_buddy = '/usr/libexec/PlistBuddy'
    app_info_plist_path = '%s/Products/Applications/%s.app' % (archive_path, SCHEME)
    os.system('cd %s' % app_info_plist_path)
    # Version
    os.system('%s -c "print CFBundleShortVersionString" %s/Info.plist' % (plist_buddy, app_info_plist_path))
    # Build
    os.system('%s -c "print CFBundleVersion" %s/Info.plist' % (plist_buddy, app_info_plist_path))
    # Bundle Identifier
    bundle_identifier_tmp = os.popen(
        '%s -c "print CFBundleIdentifier" %s/Info.plist' % (plist_buddy, app_info_plist_path)).read()
    # 当前target的名字
    projec_name_tmp = os.popen(
        '%s -c "print CFBundleExecutable" %s/Info.plist' % (plist_buddy, app_info_plist_path)).read()
    print(bundle_identifier_tmp, projec_name_tmp)
    # app的名字
    os.system('%s -c "print CFBundleDisplayName" %s/Info.plist' % (plist_buddy, app_info_plist_path))
