#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-


import os
from plistlib  import *
import time
from createPhoneList import *
from RecommendGUI import *

print("======打包正式开始======")

# 项目路径 [需修改]
projectDir="/Users/admin/ios/"

# 打包输出路径
ipaDir = "/Users/admin/Desktop/生成的ipa包/"

# 项目target [需修改]
target = "rongtuojinrong"

# 项目scheme [需修改]
scheme = "rzjrapp"

# 项目名称
projectName = "fmapp"

# 项目绝对路径
projectApath = projectDir + projectName + ".xcodeproj"

# 项目编译后的路径
projectBpath = ipaDir + scheme + ".xcarchive"

# 编译后app中的info.plist文件路径
infoPath = projectBpath + "/Products/Applications/" + scheme + ".app/info.plist"

# 编译后app的文件路径
appPath = projectBpath + "/Products/Applications/" + scheme + ".app"

# 重新签名需要的plist文件  DistributionSummary.plist
codeSignPlistPath = ipaDir + "DistributionSummary.plist"

# 导出ipa包需要的plist文件 ExportOptions.plist
exportPlistPath = ipaDir + "ExportOptions.plist"

# teamName  [需修改] Shanghai Runrui Financial Service Co., Ltd.
teamName = "\"Shanghai Runrui Financial Service Co., Ltd.\""



# 需要修改的手机号 根据业务需求改变 ["110","120","130"]
phoneList = ["110","120","130"]
#packPkg("/Users/admin/Desktop/推荐人20180301.xlsx")

print ("phoneList的值是：",phoneList)

'''
导出ipa包的时候 用到的描述文件必须是手动创建的 然后安装到xcode中
不能用xcode的自动管理生成的
'''

# 项目记时开始
time_start=time.time()
# 编译命令 /Users/admin/RT-VS-2017-06\ 2月7号上线版本/build/rzjrapp.xcarchive
# xcodebuild archive -project /Users/admin/iosfmapp.xcodeproj -schemerzjrapp -archivePath/Users/admin/Desktop/生成的ipa包rzjrapp.xcarchive
buildCommand = "xcodebuild archive -project " + projectApath + " -scheme " + scheme + " -archivePath " +  projectBpath

#buildCommand = "xcodebuild -workspace "+projectApath+" -scheme " + scheme + " -configuration Release archive " \
#               "-archivePath  "+projectBpath+" -destination generic/platform=iOS"

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
    codesignCommand = "codesign -f -s " + teamName + " --entitlements " + codeSignPlistPath + " " + appPath
    print("执行签名命令: " + codesignCommand)
    output = os.system(codesignCommand)
    if output == 0:
        print("====================项目    <<" + n + ">>  重新签名成功,正在打包中====================")
#xcodebuild -exportArchive -archivePath /Users/admin/Desktop/生成的ipa包/rzjrapp.xcarchive -exportPath /Users/admin/Desktop/生成的ipa包/120 -exportOptionsPlist /Users/admin/Desktop/生成的ipa包/ExportOptions.plist
        exportCommand = "xcodebuild -exportArchive -archivePath " + projectBpath + " -exportPath " + ipaDir + n + " -exportOptionsPlist " + exportPlistPath
#        exportCommand = "xcodebuild -exportArchive -archivePath " + projectBpath + " -exportPath " + projectDir + n + " -exportOptionsPlist " + exportPlistPath
        print("执行打包命令: " + exportCommand)
        result = os.system(exportCommand)
        if result == 0:
            print("====================项目    <<" + n + ">>  导出成功！！！====================")
    else:
        print("====================项目    <<" + n + ">>  重新签名失败,请检查DistributionSummary.plist文件====================")
        break

time_end=time.time()
print("====================项目耗时:", time_end-time_start)



























