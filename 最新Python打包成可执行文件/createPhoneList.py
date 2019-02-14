#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 创建 plist 文件

from PackPackage import *

def createPlist(outputPath):
    # 获取用户的家目录
    homePath = os.path.expanduser("~")
    print("获取用户的家目录", homePath)
    finalPath = homePath + "/Desktop/生成的ipa包"
    print("用户输入路径是空时的文件", finalPath)
    # 输出路径
    if outputPath == '': #/Users/admin/Desktop/生成的ipa包"
        outputPath = finalPath
        if os.path.exists(outputPath):
            shutil.rmtree(outputPath) #删除文件夹和文件夹里面的内容
        # 创建
        os.makedirs(outputPath)
    print("修改的IPA的输出地址是", outputPath)

    # 在输出路径中创建DistributionSummary.plist
    # 创建 architectures 数组
    architectures = ["armv7", "arm64"]
    # 创建 certificate 字典
#    certificate = {"SHA1":"65837FB1B1F0EB85E686D9603124B711E9903495","dateExpires":"2020/10/8","type":"iOS Distribution"}
    certificate = {"SHA1": "7946EE36C749575B27C31120C59191FE88061258", "dateExpires": "2018/11/26", "type": "iOS Distribution"}
    # 创建 entitlements 字典  , "keychain-access-groups": ["HKYG7W22CW.*"]
    entitlements = {"application-identifier": "HKYG7W22CW.com.ios.rongtuoDevTestNew", "aps-environment": "production", "com.apple.developer.team-identifier": "HKYG7W22CW", "com.apple.security.application-groups": [], "get-task-allow": False}
    # com.apple.security.application-groups:App Groups 数组
    # 创建 profile 字典
#    profile  = {"UUID":"201842be-9065-410f-a19a-51de52277512","name":"iOS Team Inhouse Provisioning Profile: com.ios.rongtuoDevTestNew"}
    profile  = {"UUID": "e322a7d8-bd8e-4516-b64a-c7695de6bde6", "name": "com.ios.rongtuoDevTestNew"}
    # 创建 team 字典
    team = {"id": "HKYG7W22CW", "name": " Shanghai Runrui Financial Service Co., Ltd."}
    summaryDict = {"architectures": architectures, "certificate": certificate, "entitlements": entitlements, "name": "rzjrapp.app","profile":profile,"team":team}
    summary = [summaryDict]
    Root = {"rzjrapp.ipa": summary}
    print("\n DistributionSummary.plist里面:\n", Root)
    # writePlist(Root, outputPath + "/DistributionSummary.plist")
    
    # 在输出路径中创建ExportOptions.plist  "uploadSymbols": False, "signingCertificate": "iPhone Distribution", automatic  manual
    provisioningProfiles = {"com.ios.rongtuoDevTestNew": "com.ios.rongtuoDevTestNew"}
    exportOptionsRoot = {"compileBitcode": False, "destination": "export", "method": "enterprise", "uploadSymbols": False, "signingCertificate": "iPhone Distribution", "provisioningProfiles": provisioningProfiles, "signingStyle": "automatic", "stripSwiftSymbols": True, "teamID": "HKYG7W22CW", "thinning": "<none>"}
    writePlist(exportOptionsRoot, outputPath + "/ExportOptions.plist")

    return outputPath

# 获取推荐人 userid: excel路径，工程路径，输出路径
def packPkg(excelFile, projectFile, outputPath, infoPlistPath):
    print("推荐人excel地址是", excelFile) #/Users/admin/Desktop/推荐人20180301.xlsx
    print("ipa包地址是", projectFile) #/Users/admin/ios/fmapp.xcodeproj
    print("IPA的输出地址是", outputPath) #/Users/admin/Desktop/生成的ipa包
    print("infoPlistPath的输出地址是", infoPlistPath) # /Users/admin/ios/fmapp/registerPhone.plist
    
    # 获取输出路径
    outputPath = createPlist(outputPath)
    
    # 读取表格
    excel_data = xlrd.open_workbook(excelFile)
    # 取出Excel的第一个sheet数据
    table_one = excel_data.sheet_by_index(0) # 根据sheet索引获取sheet的内容
    # 表格的总行数
    lines = table_one.nrows
    cols = table_one.ncols
    print("表格的总行数:", lines)
    print("表格的总列数:", cols)
    last_output_dir = ''
    
    idList = []
    infoPlist = []
    
    for i in range(0,lines):
        # 获取excel表格一行的数据
        row_values = table_one.row_values(i)
        tuijianren_id = str(int(row_values[0]))
        
        tuijianren_phone = str(int(row_values[1]))
        
        dict = {"fmuserid": tuijianren_id, "fmmobile": tuijianren_phone}
        
        idList.append(tuijianren_id)
        # 将Excel表格中的数据转成数组
        infoPlist.append(dict)
        
    # 删除旧的plist数据，导入新的
    plist = readPlist(infoPlistPath)
    print ("原plist是：", plist)
    writePlist(infoPlist, infoPlistPath)

    print("===========创建的列表是：",idList)
    print("读取的手机号列表是：", infoPlist)
    plist = readPlist(infoPlistPath)
    print("修改之后的列表是：", plist)
#    # 选择Xcode的版本打包
#    identifier = "" # 标识符 iphoneos11.1
#    if identifier == "iphoneos11.1": # Xcode9.1
#        os.system("sudo xcode-select --switch /Users/admin/Downloads/Xcode.app/Contents/Developer/")
#    else:
#     os.system("sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer/")

    if len(idList) == lines:
        # 调用打包程序
        beginToPackage(projectFile, outputPath, idList)
    else:
        print ("读取Excel失败")

# 修改打包好的ipa的名字：app109
# outputPath:所有的ipa包的文件夹的上层文件夹 /Users/admin/Desktop/生成的ipa包
# path:打包好的ipa包的文件夹路径 /Users/admin/Desktop/生成的ipa包/120
def changeFileName(exportPath, outputPath):
    if not os.path.isdir(exportPath):
        return False
    if os.path.isdir(exportPath):
        fileName = os.path.basename(exportPath)
        pathOld = exportPath + "/rzjrapp.ipa"
        print ("获取文件名：",fileName)
        pathNew = exportPath + "/app" + fileName + ".ipa"
        os.rename(pathOld , pathNew)
#        # 将所有的ipa包移动到统一的文件夹
#        ipaPath = os.makedirs(outputPath + "/所有的ipa包")
        #将要移动的文件夹
        pathMoved = outputPath + "/所有的ipa包"
        shutil.move(pathNew, pathMoved)

