#!C:\Python27\python.exe
# coding=utf-8

import zipfile
import shutil
import os
import xlr

import tkMessageBox

def packPkg(excelFile, apkFile, outputPath):
	# 空文件 便于写入此空文件到apk包中作为channel文件
	src_empty_file = 'info/czt.txt'
	# 创建一个空文件（不存在则创建）
	f = open(src_empty_file, 'w') 
	f.close()

	# 获取当前目录中所有的apk源包
	src_apks = [apkFile]
	# python3 : os.listdir()即可，这里使用兼容Python2的os.listdir('.')
	#for file in os.listdir('.'):
	#    if os.path.isfile(file):
	#        extension = os.path.splitext(file)[1][1:]
	#       if extension in 'apk':
	#            src_apks.append(file)

	# 获取渠道列表
	#channel_file = 'info/channel.txt'
	#f = open(channel_file)
	#lines = f.readlines()
	#f.close()
	#excel_file = 'info/tuijianren20180208.xls'
	ecl_data = xlrd.open_workbook(excelFile)
	sheet_data = ecl_data.sheets()[0]
	#表格的总行数
	lines = sheet_data.nrows
	last_output_dir = ''

	for src_apk in src_apks:
	    # file name (with extension)
	    src_apk_file_name = os.path.basename(src_apk)
	    # 分割文件名与后缀
	    temp_list = os.path.splitext(src_apk_file_name)
	    # name without extension
	    src_apk_name = temp_list[0]
	    # 后缀名，包含.   例如: ".apk "
	    src_apk_extension = temp_list[1]
    
	    # 创建生成目录,与文件名相关
	    output_dir = outputPath + '/output_' + src_apk_name + '/'
	    last_output_dir = output_dir
	    # 目录不存在则创建
	    if not os.path.exists(output_dir):
	        os.mkdir(output_dir)
        
	    # 遍历渠道号并创建对应渠道号的apk文件
	    for i in xrange(0, lines):
	        #获取excel表格一行的数据
	        row_values = sheet_data.row_values(i)
	        # 获取当前渠道号，因为从渠道文件中获得带有\n,所有strip一下
	        #target_channel = line.strip()
	        #推荐人数列 109:15069199293
	        #tuijianren = target_channel.split(":")
	        # 拼接对应渠道号的apk
	        #target_apk = output_dir + "rtjr_" + tuijianren[0] + src_apk_extension
	        tuijianren_id = str(int(row_values[0]))
	        target_apk = output_dir + "rtjr_" + tuijianren_id + src_apk_extension
	        # 拷贝建立新apk
	        shutil.copy(src_apk, target_apk)
	        # zip获取新建立的apk文件
	        zipped = zipfile.ZipFile(target_apk, 'a', zipfile.ZIP_DEFLATED)
	        # 初始化渠道信息
	        empty_channel_file = "META-INF/rtjrrecommend_{tj_id}_{tj_phone}".format(tj_id = tuijianren_id, tj_phone = row_values[1])
	        # 写入渠道信息
	        zipped.write(src_empty_file, empty_channel_file)
	        # 关闭zip流
	        zipped.close()
	result = tkMessageBox.showinfo("温馨提示", str(lines) + "个推荐人包已全部生成！")
	if result and not last_output_dir == '':
		os.startfile(last_output_dir)







