#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# FileName:PackPackage.py

from RTYX.EnterPrise.RTYXCreatePhoneList import *
import time
import subprocess
from tkinter import *
from tkinter import messagebox
import os
import shutil
from plistlib import *


# 修改打包好的ipa的名字：app109
# outputPath:所有的ipa包的文件夹的上层文件夹 /Users/admin/Desktop/生成的ipa包
# path:打包好的ipa包的文件夹路径 /Users/admin/Desktop/生成的ipa包/120
# infoPath:打包好的ipa包的Info.plist路径
def changeFileName(export_path, output_path, info_path, scheme):
    # if not os.path.exists(export_path):
    #     # 创建文件夹
    #     os.makedirs(export_path)
    if not os.path.isdir(export_path):
        return False
    if os.path.isdir(export_path):
        fileName = os.path.basename(export_path)
        pathOld = export_path + "/" + scheme + ".ipa"
        print("获取文件名：", fileName)
        pathNew = export_path + "/app" + fileName + ".ipa"
        os.rename(pathOld, pathNew)

        print("==========pathOld:", pathOld, "==========pathNew:", pathNew)

        # 将要移动的文件夹
        pathMoved = output_path + "/所有的ipa包"
        shutil.move(pathNew, pathMoved)  # 文件移动

        print("==========pathMoved:", pathMoved)
        shutil.rmtree(export_path)  # 删除文件夹和文件夹里面的内容
        # 创建这个ipa包的plist文件
        # 创建assets数组
        asserts = []
        # https://rtyx-boss.oss-cn-shanghai.aliyuncs.com/apk_download/tuijianren/ios/v110/app126.ipa
        # url = "https://www.rongtuojinrong.com/Public/file/app" + fileName + ".ipa"
        url = "https://rtyx-boss.oss-cn-shanghai.aliyuncs.com/apk_download/tuijianren/ios/v110/app" + fileName + ".ipa"
        assertsDict = {"kind": "software-package",
                       "url": url}
        asserts.append(assertsDict)
        # 创建metadata字典
        # 读取版本号
        plist = readPlist(info_path)
        version = plist["CFBundleVersion"]
        metadataDict = {"bundle-identifier": "com.rtyx.enterprise",
                        "bundle-version": version,
                        "kind": "software",
                        "title": "融托优选"}
        # 创建数组的字典和数组
        dict = {"assets": asserts, "metadata": metadataDict}
        items = [dict]
        # 创建Root字典
        Root = {"items": items}
        print("\n Root里面:\n", Root)
        writePlist(Root, pathMoved + "/app" + fileName + ".plist")

#
# # 融托优选-企业版修改工程的 bundle identifier
# def change_bundle_identifier(project_file, scheme, bundle_identifier):
#     plist_buddy = '/usr/libexec/PlistBuddy'
#     # /Users/admin/XZ公司项目/RTYX/RTYX/Info.plist
#     app_info_plist_path = '%s/%s/Config/Info.plist' % (project_file, scheme)
#     # Set :CFBundleIdentifier com.rtyx.RTYXEn
#     change_command = '%s -c "Set :CFBundleIdentifier %s"  %s' % (plist_buddy, bundle_identifier, app_info_plist_path)
#     result = os.system(change_command)
#     print("change_command:", change_command, "\n修改结果：", result)
#     if result == 0:
#         print("================= 修改 bundle indentifier 成功 =================")
#     else:
#         print("================= 修改 bundle indentifier 失败 =================")


# 融托优选- 替换 描述文件
def change_profile(archive_path, profile_path, scheme):
    # 获取到融托优选的描述文件路径  RTYXEnterpriseProfile
    rtyx_profile = os.path.abspath(profile_path)
    # 目的路径
    destination_path = archive_path + ("/Products/Applications/%s.app/embedded.mobileprovision" % scheme)
    # 替换描述文件
    shutil.copy(rtyx_profile, destination_path)


# 项目路径，打包的输出路径，
def beginToPackage(project_path, output_path, id_list):

    print("======打包正式开始======")
    project_name = os.path.basename(project_path)  # 根据全路径获取文件名称
    scheme = project_name.split('.')[0] + 'Enterprise'
    export_options_plist_path = '%s/ExportOptions.plist' % output_path
    project_file = os.path.dirname(project_path)  # 根据全路径获取文件所在路径

    archive_path = '%s/%s.xcarchive' % (output_path, scheme)  # .archive 包的导出路径

    print("==============project_file：", project_file)
    print("==============project_path：", project_path)

    # # 修改scheme
    # change_bundle_identifier(project_file, scheme, "com.rtyx.enterprise")

    # 项目记时开始
    time_start = time.time()

    xcodebuild = '/usr/bin/xcodebuild'  # 终端输入 which xcodebuild 获取路径
    # clean
    print("================= Clean =================")
    clean_comand = '%s clean -workspace %s ' \
                   '-configuration %s ' \
                   '-scheme %s' % (xcodebuild, project_path, 'Release', scheme)
    os.system(clean_comand)
    print("clean工程：", clean_comand)

    # 编译命令
    print("================= Archive =================")
    # CFBundleVersion=  -destination generic/platform=ios CODE_SIGN_IDENTITY
    archive_comand = '%s archive -workspace %s ' \
                     '-scheme %s ' \
                     '-configuration %s ' \
                     '-archivePath %s' % (xcodebuild, project_path, scheme, 'Release', archive_path)
    os.system(archive_comand)
    print("archive工程：", archive_comand)

    # 编译后app中的info.plist文件路径 rzjrapp scheme
    info_path = archive_path + "/Products/Applications/" + scheme + ".app/Info.plist"

    # 修改描述文件
    change_profile(archive_path, "RTYXEnterpriseProfile/embedded.mobileprovision", scheme)

    if os.path.exists(output_path + "/所有的ipa包"):
        shutil.rmtree(output_path + "/所有的ipa包")  # 删除文件夹和文件夹里面的内容
    # 创建ipa包
    os.makedirs(output_path + "/所有的ipa包")

    for n in id_list:
        # 修改plist文件
        pl = readPlist(info_path)
        # 修改对应的业务数据
        pl["LocalUserID"] = n
        writePlist(pl, info_path)

        print("====================项目   <<" + n + ">>  正在导出中====================")
        # export ipa
        exportPath = output_path + "/" + n
        export_comand = '%s -exportArchive -archivePath %s ' \
                        '-exportPath %s ' \
                        '-exportOptionsPlist %s ' \
                        '-allowProvisioningUpdates' % (
                        xcodebuild, archive_path, exportPath, export_options_plist_path)
        result = os.system(export_comand)
        print("导出工程：", export_comand)

        print('导出结果：', result)

        if result == 0:
            print("====================项目    <<" + n + ">>  导出成功！！！====================")
            print("============exportPath:", exportPath)

            changeFileName(exportPath, output_path, info_path, scheme)
        else:
            print("====================项目    <<" + n + ">>  导出失败！！！====================")

    time_end = time.time()
    print("====================项目耗时:", time_end - time_start)
    result = messagebox.showinfo("温馨提示", str(len(id_list)) + "个推荐人id已全部打包完毕！")
    if result:
        subprocess.call(["open", output_path + "/所有的ipa包"])
        sys.exit()






















