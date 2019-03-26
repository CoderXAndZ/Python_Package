#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 融托金融多个target打包

import os
import shutil
from plistlib import *


# 开始打包
def package_rtjr(project_path, scheme, configuration, method):
    # 获取用户的家目录
    home_path = os.path.expanduser("~")

    ipa_output_path = home_path + "/Desktop/RTJRipa"  # ipa 包的输出路径
    if os.path.exists(ipa_output_path):
        shutil.rmtree(ipa_output_path)  # 删除文件夹和文件夹里面的内容
    # 创建
    os.makedirs(ipa_output_path)

    project_name = os.path.basename(project_path)  # 根据全路径获取文件名称
    # scheme = project_name.split('.')[0]
    project_file = os.path.dirname(project_path)  # 根据全路径获取文件所在路径
    archive_path = '%s/%s.xcarchive' % (ipa_output_path, scheme)  # .archive 包的导出路径
    ipa_path = '%s/%s.ipa' % (ipa_output_path, scheme)
    export_options_plist_path = '%s/ExportOptions.plist' % ipa_output_path

    # 创建 ExportOptions.plist
    create_export_options_plist(export_options_plist_path, method)

    print("输出路径：", ipa_output_path)
    print("项目名称：", project_name)
    print("SCHEME：", scheme)
    print("archive_path:", archive_path)
    print("ipa_path:", ipa_path)
    print("ExportOptionsPlistPath:", export_options_plist_path, "CONFIGURATION:", configuration)

    clean_command = 'xcodebuild clean -project %s -scheme %s -configuration %s' % \
                    (project_path, scheme, configuration)

    print("执行清空项目命令: " + clean_command)
    clean_command_output = os.system(clean_command)

    if clean_command_output == 0:
        print("================= 清空成功 =================")
    else:
        print("================= 清空失败 =================")

    # 编译后app中的info.plist文件路径 rzjrapp scheme
    # info_Path = archive_path + "/Products/Applications/" + "rzjrapp" + ".app/Info.plist"
    # xcodebuild archive -sdk iphoneos11.1 -project
    build_command = "xcodebuild archive -project " + project_path + " -scheme " + scheme + \
                    " -archivePath " + archive_path + " -configuration " + configuration
    print("执行编译命令: " + build_command)
    output = os.system(build_command)

    if output == 0:
        print("================= 编译成功 =================")
        print("================= 正在导出... =================")
    else:
        print("================= 编译失败 =================")

    # 导出ipa包需要的plist文件 ExportOptions.plist
    # export_path = ipa_output_path + "/" + scheme
    export_command = "xcodebuild -exportArchive -archivePath " + archive_path + " -exportPath " + ipa_output_path + " -exportOptionsPlist " + export_options_plist_path + ' -allowProvisioningUpdates'
    print("执行导出命令: " + export_command)
    result = os.system(export_command)

    if result == 0:
        print("================= 导出成功 =================")
    else:
        print("================= 导出失败 =================")


# 创建 ExportOptions.plist 文件
def create_export_options_plist(plist_path, method):
    print("method：", method)

    if method == 'ad-hoc':  # ad-hoc包
        root_dict = {"compileBitcode": False,
                     "destination": "export",
                     "method": "ad-hoc",
                     "signingStyle": "automatic",
                     "stripSwiftSymbols": True,
                     "teamID": "J4ZY3DZS4W",
                     "thinning": "<none>"}
        with open(plist_path, "wb+") as fp:
            dump(root_dict, fp)
    elif method == 'enterprise':  # 企业版
        root_dict = {"compileBitcode": False,
                     "destination": "export",
                     "method": "enterprise",
                     "signingStyle": "automatic",
                     "stripSwiftSymbols": True,
                     "teamID": "HKYG7W22CW",
                     "thinning": "<none>"}
        with open(plist_path, "wb+") as fp:
            dump(root_dict, fp)
    else:  # App Store版本导出
        root_dict = {
            "destination": "export",
            "method": "app-store",
            "signingStyle": "automatic",
            "stripSwiftSymbols": True,
            "teamID": "J4ZY3DZS4W",
            "uploadSymbols": True
            # "uploadBitcode": False,
            # "generateAppStoreInformation": False
        }
        with open(plist_path, "wb+") as fp:
            dump(root_dict, fp)
