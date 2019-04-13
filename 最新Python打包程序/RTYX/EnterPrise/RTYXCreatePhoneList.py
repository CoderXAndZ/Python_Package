#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 创建 plist 文件

from RTYX.EnterPrise.RTYXPackage import *
import os
import shutil
import xlrd


def createPlist(output_path):
    # 获取用户的家目录
    home_path = os.path.expanduser("~")
    print("获取用户的家目录", home_path)
    final_path = home_path + "/Desktop/RTYXEnterpriseIPA包"
    print("用户输入路径是空时的文件", final_path)
    # 输出路径
    if output_path == '':  # /Users/admin/Desktop/生成的ipa包"
        output_path = final_path
        if os.path.exists(output_path):
            shutil.rmtree(output_path)  # 删除文件夹和文件夹里面的内容
        # 创建
        os.makedirs(output_path)
    print("修改的IPA的输出地址是", output_path)

    create_export_options_plist(output_path + "/ExportOptions.plist")

    return output_path


# 创建 ExportOptions.plist 文件
def create_export_options_plist(plist_path):

    root_dict = {"compileBitcode": True,
                "destination": "export",
                "method": "enterprise",
                "provisioningProfiles": {
                    "com.rtyx.enterprise": "rtyxEnterprise"
                },
                "signingStyle": "manual",
                "stripSwiftSymbols": True,
                "teamID": "HKYG7W22CW",
                "thinning": "<none>"}
    with open(plist_path, "wb+") as fp:
        dump(root_dict, fp)


# 获取推荐人 userid: excel路径，工程路径，输出路径
def packPkg(excel_file, project_file, output_path, info_plist_path):
    print("推荐人excel地址是", excel_file)  # /Users/admin/Desktop/推荐人20180301.xlsx
    print("ipa包地址是", project_file)  # /Users/admin/ios/fmapp.xcodeproj
    print("IPA的输出地址是", output_path)  # /Users/admin/Desktop/生成的ipa包
    print("infoPlistPath的输出地址是", info_plist_path)  # /Users/admin/ios/fmapp/registerPhone.plist

    # 获取输出路径
    outputPath = createPlist(output_path)

    # 读取表格
    excel_data = xlrd.open_workbook(excel_file)
    # 取出Excel的第一个sheet数据
    table_one = excel_data.sheet_by_index(0)  # 根据sheet索引获取sheet的内容
    # 表格的总行数
    lines = table_one.nrows
    cols = table_one.ncols
    print("表格的总行数:", lines)
    print("表格的总列数:", cols)
    last_output_dir = ''

    idList = []
    infoPlist = []

    for i in range(0, lines):
        # 获取excel表格一行的数据
        row_values = table_one.row_values(i)
        tuijianren_id = str(int(row_values[0]))

        tuijianren_phone = str(int(row_values[1]))

        dict = {"fmuserid": tuijianren_id, "fmmobile": tuijianren_phone}

        idList.append(tuijianren_id)
        # 将Excel表格中的数据转成数组
        infoPlist.append(dict)

    # 删除旧的plist数据，导入新的
    plist = readPlist(info_plist_path)
    print("原plist是：", plist)
    writePlist(infoPlist, info_plist_path)

    print("===========创建的列表是：", idList)
    print("读取的手机号列表是：", infoPlist)
    plist = readPlist(info_plist_path)
    print("修改之后的列表是：", plist)
    #    # 选择Xcode的版本打包
    #    identifier = "" # 标识符 iphoneos11.1
    #    if identifier == "iphoneos11.1": # Xcode9.1
    #        os.system("sudo xcode-select --switch /Users/admin/Downloads/Xcode.app/Contents/Developer/")
    #    else:
    # os.system("sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer/")
    if len(idList) == lines:
        # 调用打包程序
        beginToPackage(project_file, outputPath, idList)
    else:
        print("读取Excel失败")


# # 修改打包好的ipa的名字：app109
# # outputPath:所有的ipa包的文件夹的上层文件夹 /Users/admin/Desktop/生成的ipa包
# # path:打包好的ipa包的文件夹路径 /Users/admin/Desktop/生成的ipa包/120
# def changeFileName(export_path, output_path):
#     if not os.path.isdir(export_path):
#         return False
#     if os.path.isdir(export_path):
#         file_name = os.path.basename(export_path)
#         path_old = export_path + "/RTYX.ipa"
#         print("获取文件名：", file_name)
#         path_new = export_path + "/app" + file_name + ".ipa"
#         os.rename(path_old, path_new)
#         #        # 将所有的ipa包移动到统一的文件夹
#         #        ipaPath = os.makedirs(outputPath + "/所有的ipa包")
#         # 将要移动的文件夹
#         path_moved = output_path + "/所有的ipa包"
#         shutil.move(path_new, path_moved)

