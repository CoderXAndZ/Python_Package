#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 融托金融多个target打包

import os
import shutil
from plistlib import *
from tkinter import messagebox

# 将ipa包上传到fir_im
# ipa_path:ipa包路径,
# emails:邮件地址,多个地址英文逗号分隔
# update_description:更新内容
def post_to_fir_im(ipa_path, update_description):
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

        messagebox.showinfo("温馨提示", "打包发送firm完毕！")
    else:
        print('================= 发布失败 =================')

    # # 蒲公英上传
    # 执行 curl -F "file=@/tmp/example.ipa" -F "uKey=xxx" -F "_api_key=xxx" https://qiniu-storage.pgyer.com/apiv1/app/upload 请根据开发者自己的账号，将其中的 uKey 和 _api_key 的值替换为相应的值。


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

    # xcodebuild = '/usr/bin/xcodebuild'  # 终端输入 which xcodebuild 获取路径
    # 由于使用Xcode10.1打包，且它在文稿中，所以修改xcodebuild的路径为该Xcode10.1的xcodebuild的路径
    xcodebuild = '/Users/admin/Documents/Xcode.app/Contents/Developer/usr/bin/xcodebuild'

    # # clean
    # print("================= Clean =================")
    # clean_comand = '%s clean -workspace %s ' \
    #                '-configuration %s ' \
    #                '-scheme %s' % (xcodebuild, project_path, configuration, scheme)
    # os.system(clean_comand)
    # print("clean工程：", clean_comand)

    os.system("sudo xcode-select --switch /Users/admin/Documents/Xcode.app/Contents/Developer/")

    # archive
    print("================= Archive =================")
    # CFBundleVersion=  -destination generic/platform=ios CODE_SIGN_IDENTITY
    archive_comand = '%s archive -workspace %s ' \
                     '-scheme %s ' \
                     '-configuration %s ' \
                     '-archivePath %s' % (xcodebuild, project_path, scheme, configuration, archive_path)
    os.system(archive_comand)
    print("archive工程：", archive_comand)

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

        post_to_fir_im(ipa_path, "adhoc包")
        # messagebox.showinfo("温馨提示", "打包完毕！")
    else:
        print('================= 打包失败 =================')
    ####################### 由于使用了CocoaPod进行代码管理，因此底下代码暂不使用 #############################
    # clean_command = 'xcodebuild clean -project %s -scheme %s -configuration %s' % \
    #                 (project_path, scheme, configuration)
    #
    # print("执行清空项目命令: " + clean_command)
    # clean_command_output = os.system(clean_command)
    #
    # if clean_command_output == 0:
    #     print("================= 清空成功 =================")
    # else:
    #     print("================= 清空失败 =================")
    #
    # # 编译后app中的info.plist文件路径 rzjrapp scheme
    # # info_Path = archive_path + "/Products/Applications/" + "rzjrapp" + ".app/Info.plist"
    # # xcodebuild archive -sdk iphoneos11.1 -project
    # build_command = "xcodebuild archive -project " + project_path + " -scheme " + scheme + \
    #                 " -archivePath " + archive_path + " -configuration " + configuration
    # print("执行编译命令: " + build_command)
    # output = os.system(build_command)
    #
    # if output == 0:
    #     print("================= 编译成功 =================")
    #     print("================= 正在导出... =================")
    # else:
    #     print("================= 编译失败 =================")
    #
    # # 导出ipa包需要的plist文件 ExportOptions.plist
    # # export_path = ipa_output_path + "/" + scheme
    # export_command = "xcodebuild -exportArchive -archivePath " + archive_path + " -exportPath " + ipa_output_path + " -exportOptionsPlist " + export_options_plist_path + ' -allowProvisioningUpdates'
    # print("执行导出命令: " + export_command)
    # result = os.system(export_command)
    #
    # if result == 0:
    #     print("================= 导出成功 =================")
    #     post_to_fir_im(ipa_path, "adhoc包")
    # else:
    #     print("================= 导出失败 =================")
    ####################### 由于使用了CocoaPod进行代码管理，因此以上代码暂不使用 #############################

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
