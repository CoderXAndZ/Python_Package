#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# FileName:PackPackage.py

from RTJR.Enterprise.createPhoneList import *
import time
import subprocess
from tkinter import *
from tkinter import messagebox

## 项目target [需修改]
#target = "rongtuojinrongexport PATH="

# 项目scheme [需修改] rzjrapp rongtuojinrong
scheme = "rongtuojinrongQY"

# teamName  [需修改] Shanghai Runrui Financial Service Co., Ltd.
teamName = "\"Shanghai Runrui Financial Service Co., Ltd.\""


# 修改打包好的ipa的名字：app109
# outputPath:所有的ipa包的文件夹的上层文件夹 /Users/admin/Desktop/生成的ipa包
# path:打包好的ipa包的文件夹路径 /Users/admin/Desktop/生成的ipa包/120
# infoPath:打包好的ipa包的Info.plist路径
def changeFileName(exportPath, outputPath, infoPath):
    if not os.path.isdir(exportPath):
        return False
    if os.path.isdir(exportPath):
        fileName = os.path.basename(exportPath)
        pathOld = exportPath + "/" + scheme + ".ipa"
        print("获取文件名：", fileName)
        pathNew = exportPath + "/app" + fileName + ".ipa"
        os.rename(pathOld, pathNew)
        
        #将要移动的文件夹
        pathMoved = outputPath + "/所有的ipa包"
        shutil.move(pathNew, pathMoved) #文件移动
        shutil.rmtree(exportPath) #删除文件夹和文件夹里面的内容
        # 创建这个ipa包的plist文件
        # 创建assets数组
        asserts = []
        url = "https://www.rongtuojinrong.com/Public/file/app" + fileName + ".ipa"
        assertsDict = {"kind": "software-package",
                       "url": url}
        asserts.append(assertsDict)
        # 创建metadata字典
        # 读取版本号
        plist = readPlist(infoPath)
        version = plist["CFBundleVersion"]
        metadataDict = {"bundle-identifier": "com.ios.rongtuoDevTestNew",
                        "bundle-version": version,
                        "kind": "software",
                        "title": "融托金融"}
        # 创建数组的字典和数组
        dict = {"assets": asserts, "metadata": metadataDict}
        items = [dict]
        # 创建Root字典
        Root = {"items": items}
        print("\n Root里面:\n", Root)
        writePlist(Root, pathMoved + "/app" + fileName + ".plist")


# 项目路径，打包的输出路径，
def beginToPackage(projectpath, outputPath, idList):
    print("======打包正式开始======")
    # 项目记时开始
    time_start = time.time()
    # 清空项目  xcodebuild clean -project fmapp.xcodeproj -scheme rzjrapp -configuration Release
    clean_Command = "xcodebuild clean -project " + projectpath + " -scheme " + scheme + ' -configuration Release'
    print("执行清空项目命令: " + clean_Command)
    clean_Command_output = os.system(clean_Command)

# 编译命令
# xcodebuild archive -project /Users/admin/ios/fmapp.xcodeproj -scheme rzjrapp -archivePath /Users/admin/Desktop/生成的ipa包/rzjrapp.xcarchive
    archivePath = outputPath + "/" + scheme + ".xcarchive"
    # 编译后app中的info.plist文件路径 rzjrapp scheme
    infoPath = archivePath + "/Products/Applications/" + scheme + ".app/Info.plist"
    # xcodebuild archive -sdk iphoneos11.1 -project
    buildCommand = "xcodebuild archive -project " + projectpath + " -scheme " + scheme + " -archivePath " + archivePath

    # buildCommand = "xcodebuild -workspace "+projectpath+" -scheme " + scheme + " -configuration Release archive " \
    #   "-archivePath  "+outputPath+" -destination generic/platform=iOS"

    print("执行编译命令: " + buildCommand)
    output = os.system(buildCommand)
    
    if os.path.exists(outputPath + "/所有的ipa包"):
        shutil.rmtree(outputPath + "/所有的ipa包")  # 删除文件夹和文件夹里面的内容
    # 将所有的ipa包移动到统一的文件夹
    os.makedirs(outputPath + "/所有的ipa包")
##  changeFileName("/Users/admin/Desktop/生成的ipa包/111", "/Users/admin/Desktop/生成的ipa包","/Users/admin/Desktop/生成的ipa包/111/Payload/rzjrapp.app/Info.plist")

    for n in idList:
        # 修改plist文件
        pl = readPlist(infoPath)
        # 修改对应的业务数据
        pl["LocalUserID"] = n
        writePlist(pl, infoPath)
        # print("====================修改项目  <<" + n + ">>  plist成功,重新签名中====================")
# codesign -f -s "Shanghai Runrui Financial Service Co., Ltd." --entitlements /Users/admin/Desktop/生成的ipa包/DistributionSummary.plist /Users/admin/Desktop/生成的ipa包/rzjrapp.xcarchive/Products/Applications/rzjrapp.app
        # DistributionSummary
        # codeSignPlistPath = outputPath + "/ExportOptions.plist"
        # appPath = archivePath + "/Products/Applications/" + "rzjrapp" + ".app"  # scheme
        # archive_info_path = archivePath + "/Info.plist"
        # change_archive_info_path = readPlist(archive_info_path)
        # print("\n =========== change_archive_info_path:\n", change_archive_info_path)
        # print("\n =========== ApplicationProperties: ", change_archive_info_path["ApplicationProperties"])
        # change_archive_info_path["ApplicationProperties"]["SigningIdentity"] = "iPhone Developer: runqiu zhou(W6984V2KZV)"
        # writePlist(change_archive_info_path, archive_info_path)
        #
        # # codesignCommand = "codesign -f -s " + 'iPhone Distribution: ' + teamName + " --entitlements " + codeSignPlistPath + " " + appPath
        # # codesignCommand = "codesign -f -s " + '7946EE36C749575B27C31120C59191FE88061258' " --entitlements " + codeSignPlistPath + " " + appPath   W6984V2KZV)
        # codesignCommand = "codesign -f -s " + "iPhone Developer: runqiu zhou" + " --entitlements " + codeSignPlistPath + " " + appPath
        # print("执行签名命令: " + codesignCommand)
        # output = os.system(codesignCommand)
        output = 0
        if output == 0:
            # print("====================项目    <<" + n + ">>  重新签名成功,正在打包中====================")
#xcodebuild -exportArchive -archivePath /Users/admin/Desktop/生成的ipa包/rzjrapp.xcarchive -exportPath /Users/admin/Desktop/生成的ipa包/120 -exportOptionsPlist /Users/admin/Desktop/生成的ipa包/ExportOptions.plist
            # 导出ipa包需要的plist文件 ExportOptions.plist
            exportPlistPath = outputPath + "/" + "ExportOptions.plist"
            exportPath = outputPath + "/" + n
            exportCommand = "xcodebuild -exportArchive -archivePath " + archivePath + " -exportPath " + exportPath + " -exportOptionsPlist " + exportPlistPath + ' -allowProvisioningUpdates'
            print("执行打包命令: " + exportCommand)
            result = os.system(exportCommand)
            if result == 0:
                print("====================项目    <<" + n + ">>  导出成功！！！====================")
                # 将所有的ipa包重命名并移动到'所有的ipa包'文件夹
                print("exportPath:", exportPath)
                print("outputPath:", outputPath)
                changeFileName(exportPath, outputPath, infoPath)
#                changeFileName("/Users/admin/Desktop/生成的ipa包/111", "/Users/admin/Desktop/生成的ipa包")
        else:
            print("====================项目    <<" + n + ">>  重新签名失败,请检查DistributionSummary.plist文件====================")
    time_end = time.time()
    print("====================项目耗时:", time_end-time_start)
    result = messagebox.showinfo("温馨提示", str(len(idList)) + "个推荐人id已全部打包完毕！")
    if result:
        subprocess.call(["open", outputPath + "/所有的ipa包"])
        sys.exit()



























