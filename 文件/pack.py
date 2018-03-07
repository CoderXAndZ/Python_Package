#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-


import os
from plistlib  import *
import time


print("======打包正式开始======")

# 项目路径 [需修改]
projectDir="/Users/apple/Desktop/XWProject4/IOS/DoQuestion/"

# 项目target [需修改]
target = "DoQuestion"

# 项目scheme [需修改]
scheme = "DoQuestion"

# 项目绝对路径
projectApath = projectDir + target + ".xcworkspace"

# 项目编译后的路径
projectBpath = projectDir + target + ".xcarchive"

# 编译后app中的info.plist文件路径
infoPath = projectBpath + "/Products/Applications/"+target+".app/info.plist"

# 编译后app的文件路径
appPath = projectBpath + "/Products/Applications/"+target+".app"

# 重新签名需要的plist文件  DistributionSummary.plist
codeSignPlistPath = projectDir + "DistributionSummary.plist"

# 导出ipa包需要的plist文件 ExportOptions.plist
exportPlistPath = projectDir + "ExportOptions.plist"

# teamName  [需修改]
teamName = "\"Beijing Boao Zhongcheng Information Technology Co.,Ltd.\""

# 需要修改的手机号 根据业务需求改变
phoneList = ["110","120","130"]

'''
导出ipa包的时候 用到的描述文件必须是手动创建的 然后安装到xcode中
不能用xcode的自动管理生成的
'''

# 项目记时开始
time_start=time.time()
# 编译命令
buildCommand = "xcodebuild -workspace "+projectApath+" -scheme " + scheme + " -configuration Release archive " \
               "-archivePath  "+projectBpath+" -destination generic/platform=iOS"

print("执行编译命令: " + buildCommand)
output = os.system(buildCommand)

for n in phoneList:
    # 修改plist文件
    pl = readPlist(infoPath)
    # 修改对应的业务数据
    pl["CFBundleDisplayName"] = n;
    writePlist(pl, infoPath);
    print("====================修改项目  <<" + n + ">>  plist成功,重新签名中====================")
    codesignCommand = "codesign -f -s " + teamName + " --entitlements " + codeSignPlistPath + " " + appPath
    print("执行签名命令: " + codesignCommand)
    output = os.system(codesignCommand)
    if output == 0:
        print("====================项目    <<" + n + ">>  重新签名成功,正在打包中====================")
        exportCommand = "xcodebuild -exportArchive -archivePath " + projectBpath + " -exportPath " + projectDir + n + " -exportOptionsPlist " + exportPlistPath
        print("执行打包命令: " + exportCommand)
        result = os.system(exportCommand)
        if result == 0:
            print("====================项目    <<" + n + ">>  导出成功！！！====================")
    else:
        print("====================项目    <<" + n + ">>  重新签名失败,请检查DistributionSummary.plist文件====================")
        break

time_end=time.time()
print("====================项目耗时:", time_end-time_start)



























