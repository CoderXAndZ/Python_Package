#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-


import os
from plistlib  import *
import time
from tkinter import messagebox
import subprocess

# 项目target [需修改]
target = "rongtuojinrong"

# 项目scheme [需修改]
scheme = "rzjrapp"

# 项目名称
projectName = "fmapp"

# teamName  [需修改] Shanghai Runrui Financial Service Co., Ltd.
teamName = "\"Shanghai Runrui Financial Service Co., Ltd.\""

'''
导出ipa包的时候 用到的描述文件必须是手动创建的 然后安装到xcode中
不能用xcode的自动管理生成的
'''

# 项目路径，打包的输出路径，
def beginToPackage(projectpath, outputPath, phoneList):
    print("======打包正式开始======")
    # 项目记时开始
    time_start=time.time()
# 编译命令
# xcodebuild archive -project /Users/admin/iosfmapp.xcodeproj -scheme rzjrapp -archivePath /Users/admin/Desktop/生成的ipa包/rzjrapp.xcarchive
    archivePath = outputPath + "/" + scheme + ".xcarchive"
    # 编译后app中的info.plist文件路径
    infoPath = archivePath + "/Products/Applications/" + scheme + ".app/info.plist"
    # 编译后app的文件路径
    buildCommand = "xcodebuild archive -project " + projectpath + " -scheme " + scheme + " -archivePath " + archivePath

#buildCommand = "xcodebuild -workspace "+projectpath+" -scheme " + scheme + " -configuration Release archive " \
#               "-archivePath  "+outputPath+" -destination generic/platform=iOS"

    print("执行编译命令: " + buildCommand)
    output = os.system(buildCommand)

    for n in phoneList:
        # 修改plist文件
        pl = readPlist(infoPath)
        # 修改对应的业务数据
        pl["LocalUserID"] = n;
        writePlist(pl, infoPath);
        print("====================修改项目  <<" + n + ">>  plist成功,重新签名中====================")
# codesign -f -s "Shanghai Runrui Financial Service Co., Ltd." --entitlements /Users/admin/Desktop/生成的ipa包/DistributionSummary.plist /Users/admin/Desktop/生成的ipa包/rzjrapp.xcarchive/Products/Applications/rzjrapp.app
        codeSignPlistPath = outputPath + "/DistributionSummary.plist"
        appPath = archivePath + "/Products/Applications/" + scheme + ".app"
        codesignCommand = "codesign -f -s " + teamName + " --entitlements " + codeSignPlistPath + " " + appPath
        print("执行签名命令: " + codesignCommand)
        output = os.system(codesignCommand)
        if output == 0:
            print("====================项目    <<" + n + ">>  重新签名成功,正在打包中====================")
#xcodebuild -exportArchive -archivePath /Users/admin/Desktop/生成的ipa包/rzjrapp.xcarchive -exportPath /Users/admin/Desktop/生成的ipa包/120 -exportOptionsPlist /Users/admin/Desktop/生成的ipa包/ExportOptions.plist
       # 导出ipa包需要的plist文件 ExportOptions.plist
            exportPlistPath = outputPath + "/" + "ExportOptions.plist"
            exportCommand = "xcodebuild -exportArchive -archivePath " + archivePath + " -exportPath " + outputPath + "/" + n + " -exportOptionsPlist " + exportPlistPath
            print("执行打包命令: " + exportCommand)
            result = os.system(exportCommand)
            if result == 0:
                print("====================项目    <<" + n + ">>  导出成功！！！====================")
            else:
                print("====================项目    <<" + n + ">>  重新签名失败,请检查DistributionSummary.plist文件====================")
    time_end=time.time()
    print("====================项目耗时:", time_end-time_start)
    result = messagebox.showinfo("温馨提示", str(len(phoneList)) + "个推荐人id已全部打包完毕！" )
    if result:
        subprocess.call(["open", outputPath])




























