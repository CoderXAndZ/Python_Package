#!/usr/bin/env python
# coding=utf-8


import os
import time
import subprocess
import shutil

# plistBuddy的路径
CMD_PlistBuddy = '/usr/libexec/PlistBuddy'
#
CMD_Xcodebuild = os.popen("which xcodebuild").read()
CMD_Security = os.popen("which security").read()
CMD_Lipo = os.popen("which lipo").read()
CMD_Codesign = os.popen("which codesign").read()
# print(CMD_PlistBuddy, CMD_Xcodebuild, CMD_Security, CMD_Lipo, CMD_Codesign)

# 历史备份目录
homePath = os.path.expanduser("~")
Package_Dir = '%s/Desktop/PackageLogs' % homePath

# 脚本工作目录 Shell_File_Path
Shell_Work_Path = '/Users/mac/Z公司项目/ios'
# 用户配置
Shell_User_Xcconfig_File = '%s/user.xcconfig' % Package_Dir
# 脚本临时生成最终用于构建的配置
Tmp_Build_Xcconfig_File = '%s/build.xcconfig' % Package_Dir
Tmp_Log_File = '%s/date %s.txt' % (Package_Dir, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
# 临时文件目录
Tmp_Options_Plist_File = '%s/optionsplist.plist' % Package_Dir

global xcconfigFile

def usage():
    print('Usage:$(basename $0) -[abcdptvhx] [--enable-bitcode] [--auto-buildversion] ..."')
    print('可选项：')
    print("  -a | --archs <armv7|arm64|armv7 arm64> 指定构建架构集，例如：-a 'armv7'或者 -a 'arm64' 或者 -a 'armv7 arm64' 等")
    print("  -b | --bundle-id <bundleId> 设置Bundle Id")
    print("  -c | --channel <development|app-store|enterprise|ad-hoc> 指定分发渠道，development 内部分发，app-store商店分发，enterprise企业分发， ad-hoc 企业内部分发")
    print("  -d | --provision-dir <dir> 指定授权文件目录，默认会在~/Library/MobileDevice/Provisioning Profiles 中寻找")
    print("  -p | --keychain-password <passoword> 指定访问证书时解锁钥匙串的密码，即开机密码")
    print("  -t | --target <targetName> 指定构建的target。默认当项目是单工程(非workspace)或者除Pods.xcodeproj之外只有一个工程的情况下，自动构建工程的第一个Target")
    print("  -v | --verbose 输出详细的构建信息")
    print("  -h | --help 帮助.")
    print("  -x 脚本执行调试模式.")
    print("  --show-profile-detail <provisionfile> 查看授权文件的信息详情(development、enterprise、app-store、ad-hoc)")
    print("  --debug Debug和Release构建模式，默认Release模式，")
    print("  --enable-bitcode 开启BitCode, 默认不开启")
    print("  --auto-buildversion 自动修改构建版本号（设置为当前项目的git版本数量），默认不开启")
    print("  --env-filename <filename> 指定开发和生产环境的配置文件")
    print("  --env-varname <varname> 指定开发和生产环境的配置变量")
    print("  --env-production <YES/NO> YES 生产环境， NO 开发环境（只有指定filename和varname都存在时生效）")


# 日志格式输出，并将输出结果重定向到输出文件
def logit(string):
    # 开头部分：\033[显示方式;前景色;背景色m + 结尾部分：\033[0m
    print("\033[32m [IPABuildShell] %s \033[0m " % string)
    file_output = open(Tmp_Log_File, 'w+')
    subprocess.Popen("ipconfig", stdout=file_output)
    print("Tmp_Log_File", Tmp_Log_File)


# 错误日志格式化输出
def errorExit():
    print("\033[31m【IPABuildShell】$@ \033[0m")

    # if os.path.exists(Tmp_Log_File) is False:
    #     os.mkdir(Tmp_Log_File)
    file_output = open(Tmp_Log_File, 'w+')
    subprocess.Popen("ipconfig", stdout=file_output)
    file_output.close()


# 警告日志格式输出
def warning():
    print("\033[33m【警告】$@ \033[0m")


# 字符串版本号比较：大于等于
def versionCompareGE():
    print("字符串版本号比较：")


# 备份历史数据
def historyBackup():
    # 创建 History 文件夹
    file_History = '%s/History' % Package_Dir
    if os.path.exists(file_History) is False:
        os.mkdir(file_History)
    # 备份上一次的打包数据
    if os.path.exists(Package_Dir):
        for root, dirs, files in os.walk(Package_Dir):
            print('备份上一次的打包数据:', dirs)
            shutil.move(dirs, file_History)  # 移动文件


# 获取xcpretty安装路径
def getXcprettyPath():
    xcprettyPath = os.popen("which xcpretty").read()
    print("xcpretty安装路径", xcprettyPath)


# 创建build.xcconfig配置文件
def initBuildXcconfig():
    # os.mknod(Tmp_Build_Xcconfig_File)
    global xcconfigFile
    xcconfigFile = Tmp_Build_Xcconfig_File
    file_output = open(Tmp_Build_Xcconfig_File, 'w+')
    subprocess.Popen("ipconfig", stdout=file_output)
    file_output.close()

    print("初始化配置文件", Tmp_Build_Xcconfig_File)

def getXcconfigValue(key):
    print(key, "-getXcconfigValue")
    # return value

def initUserXcconfig():
    if os.path.exists(Tmp_Build_Xcconfig_File):
        allKeys = ['CONFIGRATION_TYPE', 'ARCHS', 'CHANNEL', 'ENABLE_BITCODE DEBUG_INFORMATION_FORMAT', 'AUTO_BUILD_VERSION', 'UNLOCK_KEYCHAIN_PWD API_ENV_FILE_NAME API_ENV_VARNAME', 'API_ENV_PRODUCTION', 'PROVISION_DIR']
        for key in allKeys:
            value = getXcconfigValue(key=key)
            if value:
                print("【初checkOpenssl始化用户配置】key = %s" % key, "value = %s" % value)
                logit()

# 检查 OpenSSL 版本
def checkOpenssl():
    opensslInfo = os.popen("openssl version").read()  # LibreSSL 2.2.7
    if opensslInfo[0:8] == 'LibreSSL' and float(opensslInfo[9:12]) <= 1.0:
        print(opensslInfo, '版本太旧，请更新 OpenSSL 版本')
    else:
        print('【构建信息】OpenSSL 版本:%s' % opensslInfo)


# 解锁keychain
def unlockKeychain(password):
    keychain_path = '%s/Library/Keychains/login.keychain' % homePath
    keychain_path_db = '%s/Library/Keychains/login.keychain-db' % homePath
    result = os.popen('%s unlock-keychain -p %s %s' % (CMD_Security, password, keychain_path)).read
    if result:
        return 1
    else:
        result1 = os.popen('%s unlock-keychain -p %s %s' % (CMD_Security, password, keychain_path_db)).read
        if result1:
            return 1
        else:
            return 0

# # 添加一项配置
# def setXCconfigWithKeyValue():


if __name__ == '__main__':
    if os.path.exists(Package_Dir) == False:
        os.mkdir(Package_Dir)

    unlockKeychain('rongtuo007')


# import os
# # import requests
# import webbrowser
# import subprocess
# import shutil
# import time
# # import commands
#
# # 打包后的ipa文件路径
# backupIPA = '/Users/mac/Desktop/生成的ipa'
# # # 应用对应蒲公英路径
# # openUrlPath = 'https://www.pgyer.com/manager/xxxxxxxxxxxxxx/app/'
# # # 应用下载页
# # openDownLoadUrlPath = 'https://www.pgyer.com/xxxxxxxxxxxxxx'
# # 项目scheme
# schemeName = 'rzjrapp'
#
# # # 蒲公英账号USER_KEY、API_KEY及App_Key
# # USER_KEY = "xxxxxxxxxxxxxx"
# # API_KEY = "xxxxxxxxxxxxxx"
# # App_Key = "xxxxxxxxxxxxxx"
#
#
# # clean工程
# def cleanPro():
#     # 开始时间
#     start = time.time()
#     if desDv == 1:
#         desDvStr = 'Release'
#     else:
#         desDvStr = 'Debug'
#     # xcodeproj工程
#     cleanProRun = 'xcodebuild clean -project %s.xcodeproj -scheme %s -configuration %s' % (
#     schemeName, schemeName, desDvStr)
#     # workspace工程
#     # cleanProRun = 'xcodebuild clean -workspace %s.xcworkspace -scheme %s -configuration %s'%(schemeName,schemeName,desDvStr)
#
#     print('%s' % cleanProRun)
#     cleanProcessRun = subprocess.Popen(cleanProRun, shell=True)
#     cleanProcessRun.wait()
#     # 结束时间
#     end = time.time()
#     # 获取Code码
#     cleanReturnCode = cleanProcessRun.returncode
#     print('%s' % cleanReturnCode)
#     if cleanReturnCode != 0:
#         print("\n***************clean失败******耗时:%s秒***************\n" % (end - start))
#     else:
#         print("\n***************clean成功*********耗时:%s秒************\n" % (end - start))
#         # archive
#         archive()
#
#
# # 编译打包流程
# def archive():
#     # 删除之前打包的ProgramIpa文件夹
#     subprocess.call(["rm", "-rf", backupIPA])
#     time.sleep(1)
#     # 在桌面上创建ProgramIpa文件夹
#     mkdir(backupIPA)
#     # subprocess.call(["mkdir","-p",backupIPA])
#     time.sleep(1)
#     # 开始时间
#     start = time.time()
#     # xcodeproj工程
#     # archiveRun = 'xcodebuild archive -project %s.xcodeproj -scheme %s -archivePath ./build/%s.xcarchive'%(schemeName,schemeName,schemeName)
#     archiveRun = 'xcodebuild archive -project %s.xcodeproj -scheme %s -archivePath %s/%s.xcarchive' % (
#     schemeName, schemeName, backupIPA, schemeName)
#     # workspace工程
#     # archiveRun = 'xcodebuild archive -workspace %s.xcworkspace -scheme %s -archivePath %s/%s.xcarchive'%(schemeName,schemeName,backupIPA,schemeName)
#
#     print('%s' % archiveRun)
#     archiveProcessRun = subprocess.Popen(archiveRun, shell=True)
#     archiveProcessRun.wait()
#     # 结束时间
#     end = time.time()
#     # 获取Code码
#     archiveReturnCode = archiveProcessRun.returncode
#     print('%s' % archiveReturnCode)
#     if archiveReturnCode != 0:
#         print("\n***************archive失败******耗时:%s秒***************\n" % (end - start))
#     else:
#         print("\n***************archive成功*********耗时:%s秒************\n" % (end - start))
#         # 导出IPA
#         exportIPA()
#
#
# def exportIPA():
#     # 开始时间
#     start = time.time()
#     # iOS8.2之前打包方式
#     # exportRun = 'xcodebuild -exportArchive -archivePath ./build/%s.xcarchive -exportPath ./build/%s -exportFormat ipa -exportProvisioningProfile "adhoc_coolfood'%(schemeName,schemeName)
#     # iOS9
#     exportRun = 'xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportOptionsPlist ./ExportOptions.plist' % (
#     backupIPA, schemeName, backupIPA, schemeName)
#     print('++++++%s' % exportRun)
#     exportProcessRun = subprocess.Popen(exportRun, shell=True)
#     exportProcessRun.wait()
#
#     # 结束时间
#     end = time.time()
#     # 获取Code码
#     exportReturnCode = exportProcessRun.returncode
#     if exportReturnCode != 0:
#         print("\n***************导出IPA失败*********耗时:%s秒************\n" % (end - start))
#     else:
#         print("\n***************导出IPA成功*********耗时:%s秒************\n" % (end - start))
#         # 切换到当前目录
#         os.chdir(backupIPA)
#         # 删除app后缀文件
#         # commands.getoutput('rm -rf ./*.xcarchive')
#         time.sleep(1)
#         # uploadIPA('%s/%s/%s.ipa' % (backupIPA, schemeName, schemeName))
#         # openDownloadUrl()
#
#
# # # 上传蒲公英
# # def uploadIPA(IPAPath):
# #     if (IPAPath == ''):
# #         print("\n***************没有找到关联IPA包*********************\n")
# #         return
# #     else:
# #         print("\n***************IPA包开始上传到蒲公英*********************\n")
# #         url = 'http://www.pgyer.com/apiv1/app/upload'
# #         data = {
# #             'uKey': USER_KEY,
# #             '_api_key': API_KEY,
# #             'installType': '2',
# #             'password': '123456',
# #             'updateDescription': des
# #         }
# #         files = {'file': open(IPAPath, 'rb')}
# #         r = requests.post(url, data=data, files=files)
#
#
# # def openDownloadUrl():
# #     # 用非系统默认浏览器打开
# #     webbrowser.open('%s%s' % (openUrlPath, App_Key), new=1, autoraise=True)
# #     time.sleep(3)
# #     webbrowser.open(openDownLoadUrlPath, new=1, autoraise=True)
# #     print("\n*************** IPA上传更新成功 *********************\n")
#
#
# # 创建backupIPA文件夹
# def mkdir(backupIPA):
#     isExists = os.path.exists(backupIPA)
#     if not isExists:
#         os.makedirs(backupIPA)
#         print(backupIPA + '创建成功')
#         return True
#     else:
#         print(backupIPA + '目录已经存在')
#         return False
#
#
# # if __name__ == '__main__'的意思是：
# # 当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；
# # 当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
# if __name__ == '__main__':
#     # des = input("请输入更新的日志描述:")
#     desDv = input('请输入编译环境 1、Release 2、Debug:')
#     # clean
#     cleanPro()