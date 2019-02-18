#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import hashlib
import uuid
import weakref
import importlib

importlib.reload(sys)

# PBX解析类
class PBXProjectHelper (object):

	def __init__(self, path):
		super(PBXProjectHelper, self).__init__()

		if os.path.exists(path):

			self.path = path
			# print "开始解析PBX路径 = %s" %path

			pbxprojFile = open(path, 'r')
			pbxprojData = pbxprojFile.read()

			# print "项目数据 = %s" %pbxprojData
			# 解释项目数据
			self.__parseDocument(pbxprojData)

			# 构造Project
			projectId = self.root["rootObject"]
			self.project = PBXProject(weakref.proxy(self), projectId, self.root ["objects"][projectId])

		else:
			print("无效的PBX路径 = %s" % path)


	# 解析文档
	def __parseDocument (self, projData) :

		pos = 0

		# 取得头描述，
		if len (projData) > 2 and projData [0] == "/" and projData [1] == "/" :

			start = pos = 2
			while len (projData) > pos and projData[pos] != "\n":
				pos += 1

			self.header = projData [start : pos].strip()
			# print "pbx header = %s" %self.header

		projData = projData[pos:]
		

		# 去除所有注释内容
		(projData, num) = re.subn ("\/\*.*?\*\/", "", projData)

		# 获取带引号值
		self.__quotValues = []
		for match in re.finditer("((\".*?\")\s*=\s*)?(\".*?\")[;|,]", projData) :
			if match :
				matchGroups = match.groups();
				if matchGroups[1] != None :
					# print "++++ quot key = %s" %matchGroups[1]
					self.__quotValues.append(matchGroups[1])
				if matchGroups[2] != None :
					# print "++++ quot value = %s" %matchGroups[2]
					self.__quotValues.append(matchGroups[2])


		# 过滤空白字符
		(projData, num) = re.subn ("\s+", "", projData)
		# print "projData = %s" %projData
		
		pos = 0
		if projData [pos] == "{" :

			(self.root, pos) = self.__parseDictionary (projData, pos + 1)
			# print "解析成功! root = %s" %self.root

		else :

			print("无效的PBX数据!")
			self.header = None
			self.root = None


	# 解析数据
	def __parseData (self, projData, start) :

		data = None
		datatype = 0

		c = projData[start]
		if c == "{" :

			# 字典
			datatype = 1
			(data, end) = self.__parseDictionary (projData, start + 1)

		elif c == "(" :

			# 数组
			datatype = 2
			(data, end) = self.__parseArray (projData, start + 1)

		else :

			# 单值
			datatype = 3
			(data, end) = self.__parseSimpleValue (projData, start)


		return data, datatype, end

	# 解析字典数据
	def __parseDictionary (self, projData, start) :
		
		dictValue = {}
		end = start

		# print "++++++++++start dict"
		while len (projData) > end and projData [end] != "}" :
			
			(key, value, end) = self.__parseKeyValuePair (projData, end)
			if key :
				# print "key = %s, value = %s" %(key, value)
				dictValue [key] = value	

		if len (projData) > end + 1 and (projData [end + 1] == ";" or projData [end + 1] == ",") :
			end += 1

		# print "++++++++++end dict"

		return dictValue, end + 1 

	# 解析字典的键值对
	def __parseKeyValuePair (self, projData, start) :
		
		key = None
		value = None
		end = start
		isQuotStart = False

		if projData[end] == "\"" :
			end += 1
			isQuotStart = True

		while len (projData) > end :

			hasFindKey = False

			if isQuotStart :

				if projData[end] == "\"" :
					end += 1
					hasFindKey = True

			elif projData [end] == "=" :

				hasFindKey = True

			if hasFindKey :
				key = projData [start : end]
				# print "find key = %s" %key
				if isQuotStart :
					key = self.__quotValues [0]
					# print "==== quot key = %s" %(key)
					del self.__quotValues [0]

				
				# 获取值
				(value, datatype, end) = self.__parseData (projData, end + 1)
				break

			else :
				
				end += 1

		return (key, value, end)

	# 解析数组数据
	def  __parseArray (self, projData, start) :

		arrayValue = []
		end = start

		# print "================start array"
		while len (projData) > end and projData [end] != ")" :

			(elm, datatype, end) = self.__parseData (projData, end)
			if elm :
				# print "elm = %s" %elm
				arrayValue.append (elm)

		if len (projData) > end + 1 and (projData [end + 1] == ";" or projData [end + 1] == ",") :
			end += 1

		# print "================end array"

		return arrayValue, end + 1



	# 解析一个简单值
	def  __parseSimpleValue (self, projData, start):
		
		value = None
		end = start
		isQuotStart = False

		if projData [end] == "\"" :
			end += 1
			isQuotStart = True

		while len (projData) > end :

			if isQuotStart :

				if projData[end] == "\"" and (projData[end + 1] == ";" or projData[end + 1] == ","):
					end += 1
					break
				else :
					end += 1

			elif projData[end] == ";" or projData[end] == "," :

				break

			else :

				end += 1

		if end > start :

			value = projData [start : end]

			if isQuotStart :
				value = self.__quotValues [0]
				# print "==== quot value = %s" %(value)
				del self.__quotValues [0]

		return value, end + 1

	# 转换值为字符串
	def __valueToString(self, value, indent):
		
		if isinstance (value, dict) :
			return self.__dictToString (value, indent)
		elif isinstance (value, list) :
			return self.__listToString (value, indent)
		else :
			return self.__simpleValueToString (value, indent)

	# 转换简单值为字符串
	def __simpleValueToString(self, data, indent):
		return data

	# 转换数组为字符串
	def __listToString(self, data, indent):
		text = "(\n"

		indent += "\t"
		for value in data :
			text += indent + self.__valueToString (value, indent) + ",\n"

		indent = indent [0 : len (indent) - 1]
		text += indent + ")"
		
		return text

	# 转换字典为字符串
	def __dictToString(self, data, indent) :

		text = "{\n"

		indent += "\t"
		for (k,v) in data.items() :
			text += indent + k + " = " + self.__valueToString (v, indent) + ";\n"

		indent = indent [0 : len (indent) - 1]
		text += indent + "}"

		return text

	# 创建唯一ID
	def genObjectId(self):
		examplehash = "D04218DC1BA6CBB90031707C"
		# uniquehash = hashlib.sha224(name).hexdigest().upper()
		# uniquehash = uniquehash[:len(examplehash) - 4]
		# return '365' + uniquehash

		uid = str(uuid.uuid1 ())
		(uid, num) = re.subn ("-", "", uid)
		uid = uid.upper ()
		return uid [:len(examplehash)]

	# 保存修改
	def save (self) :

		indent = ""
		projData = "// " + self.header + "\n"

		projData += self.__dictToString (self.root, indent)
		# print projData

		# 写入到文件
		project_file = open(self.path, 'w')
		project_file.write(projData)

	# 获取字符串值，主要提取字符串中带有双引号问题括住内容问题
	def getStringValue(self, value):

		for match in re.finditer("^\"?([^\"]*)\"?$", value) :
			if  match :
				return match.groups()[0]

		return value

	# 转换为字符串，如果输入字符串中包含空白字符或者+特殊字符，则需要添加双引号
	def converToString(self, value):

		pattern = re.compile('[\s+]')
		match = pattern.search(value)
		if match :
			return ''.join(["\"", value, "\""])
		return value

	# 获取对象
	# @param objId 对象标识
	# @param project 项目对象
	def getObject(self, objId):

		if objId in self.root["objects"] :
			obj = self.root["objects"][objId]
			isa = obj["isa"]
			if isa == "PBXProject" :
				return PBXProject(weakref.proxy(self), objId, obj)
			elif isa == "PBXGroup" :
				return PBXGroup(weakref.proxy(self), objId, obj)
			elif isa == "PBXFileReference" :
				return PBXFileReference(weakref.proxy(self), objId, obj)
			elif isa == "PBXVariantGroup" :
				return PBXVariantGroup(weakref.proxy(self), objId, obj)
			elif isa == "PBXBuildFile" :
				return PBXBuildFile(weakref.proxy(self), objId, obj)
			elif isa == "PBXNativeTarget" :
				return self.project._createTarget(objId)
			elif isa == "PBXSourcesBuildPhase" :
				return PBXSourcesBuildPhase(weakref.proxy(self), objId, obj)
			elif isa == "PBXFrameworksBuildPhase" :
				return PBXFrameworksBuildPhase(weakref.proxy(self), objId, obj)
			elif isa == "PBXResourcesBuildPhase" :
				return PBXResourcesBuildPhase(weakref.proxy(self), objId, obj)
			elif isa == "PBXShellScriptBuildPhase" :
				return PBXShellScriptBuildPhase(weakref.proxy(self), objId, obj)
			elif isa == "XCConfigurationList" :
				return XCConfigurationList(weakref.proxy(self), objId, obj)
			elif isa == "XCBuildConfiguration" :
				return XCBuildConfiguration(weakref.proxy(self), objId, obj)

		return None

	# 设置对象
	def setObject(self, obj):

		if obj.objectId not in self.root["objects"] :
			self.root["objects"][obj.objectId] = obj.data

	# 移除对象
	def delObject(self, obj):

		if obj.objectId in self.root["objects"] :
			del self.root["objects"][obj.objectId]


# 基础对象
class PBXObject (object) :

	def __init__(self, helper, objId, data) :
		super (PBXObject, self).__init__()
		self.objectId = objId
		self.data = data
		self.helper = helper

	def getISA(self):

		if "isa" in self.data :
			return self.helper.getStringValue(self.data["isa"])
		return None

	def setISA(self, isa):
		self.data["isa"] = isa

# 源路径位置
class PBXSourceTree (object) :
	GROUP = "\"<group>\""
	ROOT = "SOURCE_ROOT"
	SDK_ROOT = "SDKROOT"
	BUILD_PRODUCT = "BUILT_PRODUCTS_DIR"

# 编译设置
class XCBuildConfiguration(PBXObject):

	def __init__(self, helper, objId, data):
		PBXObject.__init__(self, helper, objId, data)

	def getName(self):

		if "name" in self.data :
			return self.helper.getStringValue(self.data["name"])
		return None

	def setName(self, name):
		self.data["name"] = name

	# 获取编译配置
	# @param name 配置名称
	def getBuildSetting(self, name):

		if "buildSettings" in self.data and name in self.data["buildSettings"]:
			return self.data["buildSettings"][name]
		return None

	# 设置编译配置
	# @param name 配置名称
	# @param settingValue 设置值
	def setBuildSetting(self, name, settingValue):
		self.data["buildSettings"][name] = settingValue

	# 添加Framework搜索路径
	# @param path 搜索路径
	def addFrameworkSearchPath (self, path) :

		if path == None :
			return

		searchPaths = self.getBuildSetting("FRAMEWORK_SEARCH_PATHS")
		if searchPaths == None :
			searchPaths = []

		if path not in searchPaths:
			searchPaths.append (path)
			self.setBuildSetting("FRAMEWORK_SEARCH_PATHS", searchPaths)


	# 添加Library搜索路径
	# @param path 搜索路径
	# @param target 编译目标，如果为None，则表示获取项目的根配置信息
	# @param scheme 模式：Debug、Release或者其他
	def addLibrarySearchPath (self, path) :

		if path == None :
			return

		searchPaths = self.getBuildSetting("LIBRARY_SEARCH_PATHS")
		if searchPaths == None :
			searchPaths = []

		if path not in searchPaths:
			searchPaths.append (path)
			self.setBuildSetting("LIBRARY_SEARCH_PATHS", searchPaths)


	# 添加Other Linker Flag
	# @param flag 标识
	def addOtherLinkerFlag (self, flag):

		if flag == None :
			return

		flags = self.getBuildSetting("OTHER_LDFLAGS")
		if flags == None :
			flags = []

		if flag not in flags :
			flags.append(flag)
			self.setBuildSetting("OTHER_LDFLAGS", flags)

# 配置列表
class XCConfigurationList(PBXObject):

	def __init__(self, helper, objId, data):
		PBXObject.__init__(self, helper, objId, data)

		self.buildConfigurations = []
		buildConfigIds = self.data["buildConfigurations"]
		for confId in buildConfigIds:
			self.buildConfigurations.append(XCBuildConfiguration(helper, confId, helper.root["objects"][confId]))
		
	def getDefaultConfigurationIsVisible(self):

		if "defaultConfigurationIsVisible" in self.data :
			return self.data["defaultConfigurationIsVisible"]
		return None

	def setDefaultConfigurationIsVisible(self, defaultConfigurationIsVisible):
		self.data["defaultConfigurationIsVisible"] = defaultConfigurationIsVisible

	def getDefaultConfigurationName(self):

		if "defaultConfigurationName" in self.data :
			return self.helper.getStringValue(self.data["defaultConfigurationName"])
		return None

	def setDefaultConfigurationName(self, defaultConfigurationName):
		self.data["defaultConfigurationName"] = defaultConfigurationName


# 导航项目
class PBXNavigatorItem (PBXObject) :

	def __init__(self, helper, objId, data):
		PBXObject.__init__(self, helper, objId, data)

	# 获取文件引用路径
	def getPath(self):

		if "path" in self.data :
			return self.helper.getStringValue(self.data["path"])
		return None

	# 设置文件引用路径
	def setPath(self, path) :
		self.data["path"] = path

	# 获取条目名称
	def getName(self):

		if "name" in self.data :
			return self.helper.getStringValue(self.data["name"]);
		return None

	# 设置条目名称
	def setName(self, name):
		self.data["name"] = name

	def getSourceTree(self):

		if "sourceTree" in self.data :
			return self.helper.getStringValue(self.data["sourceTree"])
		return None

	def setSourceTree(self, sourceTree):
		self.data["sourceTree"] = sourceTree


# 分组
class PBXGroup (PBXNavigatorItem):

	def __init__(self, helper, objId, data):
		PBXNavigatorItem.__init__(self, helper, objId, data)

		if "children" in self.data :
			self.children = []
			childObjIds = self.data["children"]
			for objId in childObjIds:
				
				if objId in helper.root["objects"] :
					obj = helper.root["objects"][objId]
					item = None
					if obj["isa"] == "PBXFileReference" :
						item = PBXFileReference(helper, objId, obj)
					elif obj["isa"] == "PBXGroup" :
						item = PBXGroup(helper, objId, obj)
					elif obj["isa"] == "PBXVariantGroup" :
						item = PBXVariantGroup(helper, objId, obj)

					if item != None :
						item.parent = self
						self.children.append(item)
				else :
					print("miss group id = %s" % objId)

	# 获取匹配名字的子项集合
	# @param curItem 当前查找父级节点
	# @param name 名称
	# @param outputChildren 输出的子节点集合
	# @param recurive 是否递归子项目
	def __getChildren(self, curItem, name, outputChildren, recurive=False) :

		if curItem.children != None :
			for child in curItem.children :
				if child.getName() == name or child.getPath() == name :
					outputChildren.append(child)
				if recurive and child.getISA() == "PBXGroup":
					self.__getChildren(child, name, outputChildren, recurive)

	# 获取子项
	# @param curItem 当前查找父级节点
	# @param name 名称
	# @param recurive 是否递归子项目
	# @return 子项对象，不存在则返回None
	def __getChild(self, curItem, name, recurive=False) :

		if curItem.children != None :
			for child in curItem.children :
				if child.getName() == name or child.getPath() == name :
					return child
				elif recurive and child.getISA() == "PBXGroup":
					tmpItem =  self.__getChild(child, name, recurive)
					if tmpItem != None :
						return tmpItem

		return None

	# 移除节点
	# @param navigatorItem 导航条目对象
	def __removeChild(self, navigatorItem) :

		if navigatorItem == None :
			return

		if navigatorItem in self.children :

			# 移除节点的所有子项
			if (navigatorItem.getISA() == "PBXGroup" or navigatorItem.getISA() == "PBXVariantGroup") and navigatorItem.children != None :

				# 如果为PBXVariantGroup则需要移除分组在Build Phase中的设置
				if navigatorItem.getISA() == "PBXVariantGroup" :
					for target in self.helper.project.targets :
						for buildPhase in target.buildPhases :
							buildPhase.removeBuildFile(navigatorItem)

				# 移除子节点
				for child in navigatorItem.children :
					navigatorItem.__removeChild(child)

			elif navigatorItem.getISA() == "PBXFileReference" :
				
				# 移除所有与其相关的BuildFile
				for target in self.helper.project.targets :
					for buildPhase in target.buildPhases :
						buildPhase.removeBuildFile(navigatorItem)
						
			print("remove child  = %s" %navigatorItem.objectId)
			navigatorItem.parent = None
			self.data["children"].remove(navigatorItem.objectId)
			self.helper.delObject(navigatorItem)
		


	# 获取子项
	# @param name 名称
	# @param recurive 是否递归子项目
	# @return 子项对象，不存在则返回None
	def getChild(self, name, recurive=False):
		return self.__getChild(self, name, recurive)

	# 查找路径
	# @param path 路径
	# @return 指定路径下的对象，如果不存在则返回None
	def find(self, path):

		item = None

		if path.startswith("//") :
			# 匹配所有子节点
			targetPath = path[2:];
			pathComponets = targetPath.split("/")

			# 先找出所有符合的路径
			matchItems = []
			self.__getChildren(self, pathComponets[0], matchItems, True)
			for matchItem in matchItems :

				hasExists = True
				tmpItem = matchItem

				for x in xrange(1,len(pathComponets)):
					pathComp = pathComponets[x]
					if len(pathComp) > 0 :
							tmpItem = tmpItem.getChild(pathComp)
							if tmpItem == None :
								hasExists = False
								break

				if hasExists :
					item = tmpItem
					break

		else :

			for match in re.finditer("[.]?\/?(.*)", path) :
				if  match :
					targetPath = match.groups()[0]
					pathComponets = targetPath.split("/")

					item = self
					for pathComp in pathComponets :
						if len(pathComp) > 0 :
							item = item.getChild(pathComp)
							if item == None :
								break
					break

		return item

	# 添加导航条目
	# @param navigatorItem 导航条目对象
	# @return 被添加的导航条目
	def addChild(self, navigatorItem):
		
		if navigatorItem == None :
			return None

		#设置对象
		self.helper.setObject(navigatorItem)

		if self.children == None :
			self.children = []
			self.data["children"] = []

		# 判断是否已经存在
		hasExists = False
		for child in self.children :
			if child.objectId == navigatorItem.objectId :
				hasExists = True
				navigatorItem = child
				break

		if not hasExists :
			navigatorItem.parent = self
			self.children.append(navigatorItem)
			self.data["children"].append (navigatorItem.objectId)

		return navigatorItem

	# 移除分组信息
	# @param navigatorItem 导航条目对象
	def removeChild (self, navigatorItem) :
		
		self.__removeChild(navigatorItem);
		self.children.remove(navigatorItem)

	# 添加分组
	# @param name 分组名称
	# @param path 路径
	# @param sourceTree 源位置
	# @return 返回被添加的分组对象
	def addGroup(self, name, path = None, sourceTree = PBXSourceTree.GROUP):

		if name == None :
			return None

		groupInfo = {}
		groupInfo ["isa"] = "PBXGroup"
		groupInfo ["name"] = self.helper.converToString(name)
		groupInfo ["sourceTree"] = sourceTree
		groupInfo ["children"] = []
		if path != None :
			groupInfo["path"] = path

		group = PBXGroup(self.helper, self.helper.genObjectId(), groupInfo)
		return self.addChild(group)

	# 添加可变分组，用于放入本地化资源文件
	# @param name 分组名称
	# @param sourceTree 源位置
	def addVariantGroup(self, name, sourceTree = PBXSourceTree.GROUP):
		
		if name == None :
			return None

		groupInfo = {}
		groupInfo ["isa"] = "PBXVariantGroup"
		groupInfo ["name"] = self.helper.converToString(name)
		groupInfo ["sourceTree"] = sourceTree
		groupInfo ["children"] = []

		group = PBXVariantGroup(self.helper, self.helper.genObjectId(), groupInfo)
		return self.addChild(group)

	# 添加系统框架
	# @param frameworkName 框架名称
	# @param target 项目Target对象
	# @param required 是否为强依赖
	def addSystemFramework (self, frameworkName, target, required = True) :
		
		return self.addFramework('System/Library/Frameworks/' + frameworkName, target, required, PBXSourceTree.SDK_ROOT)

	# 添加框架
	# @param frameworkPath 框架路径
	# @param target 项目Target对象
	# @param required 是否为强依赖
	# @param sourceTree 源位置
	def addFramework (self, frameworkPath, target, required = True, sourceTree = PBXSourceTree.GROUP) :

		settings = None
		if not required :
			settings = {}
			settings["ATTRIBUTES"] = []
			settings["ATTRIBUTES"].append("Weak")

		return self.addFile (frameworkPath, target, sourceTree, settings)

	# 添加系统动态库
	# @param dylibName  动态库名称
	# @param target 项目Target对象
	# @param required 是否为强依赖
	def addSystemDylib (self, dylibName, target, required = True) :

		return self.addDylib ("usr/lib/" + dylibName, target, required, PBXSourceTree.SDK_ROOT)

	# 添加动态库
	# @parma dylib  动态库路径
	# @param target 项目Target对象
	# @param required 是否为强依赖
	# @param souceTree 源位置
	def addDylib (self, dylibPath, target, required = True, sourceTree = PBXSourceTree.GROUP) :

		settings = None
		if not required :
			settings = {}
			settings["ATTRIBUTES"] = []
			settings["ATTRIBUTES"].append("Weak")

		return self.addFile (dylibPath, target, sourceTree, settings)

	# 添加静态库
	# @param staticLibPath 静态库路径
	# @param target 项目Target对象
	# @param souceTree 源位置
	def addStaticLib (self, staticLibPath, target, required = True, sourceTree = PBXSourceTree.GROUP) :

		settings = None
		if not required :
			settings = {}
			settings["ATTRIBUTES"] = []
			settings["ATTRIBUTES"].append("Weak")

		return self.addFile (staticLibPath, target, sourceTree, settings)

	# 添加头文件
	# @param headerFilePath 头文件路径
	# @param souceTree 源位置
	def addHeaderFile (self, headerFilePath, sourceTree = PBXSourceTree.GROUP) :
		return self.addFile (headerFilePath, None, sourceTree)


	# 添加Bundle
	# @param bundlePath 资源包路径
	# @param target  项目Target对象
	# @param souceTree 源位置
	def addBundle (self, bundlePath, target, sourceTree = PBXSourceTree.GROUP) :
		return self.addFile (bundlePath, target, sourceTree)

	# 添加本地化文件
	# @param stringsPath  strings文件路径
	# @param lang 语言
	# @param target 项目的Target对象
	# @param sourceTree 源位置
	# @return 本地化文件对象
	def addLocalizedFile (self, stringsPath, lang, target, sourceTree = PBXSourceTree.GROUP) :

		name = os.path.basename(stringsPath)

		varGroup = self.getChild(name, False)
		if varGroup == None:
			varGroup = self.addVariantGroup(name)
			target.resourceBuildPhase.addBuildFile(varGroup)

		varGroup.addLocalizedFile(stringsPath, lang, sourceTree)

	# 添加文件
	# @param path 文件路径
	# @param target 项目的Target对象
	# @param sourceTree 源位置
	# @param settings 设置，目前只对framework有效
	# @return 文件对象
	def addFile (self, path, target, sourceTree = PBXSourceTree.GROUP, settings=None) :

		name = os.path.basename(path)
		ext = None
		pathComp = os.path.splitext(path)
		if len(pathComp) > 1 :
			ext = pathComp [1].lower()

		fileTypeMapping = {
			".c" 			: "sourcecode.c.c",
			".cpp" 			: "sourcecode.cpp.cpp",
			".hpp" 			: "sourcecode.cpp.h",
			".h" 			: "sourcecode.c.h",
			".swift" 		: "sourcecode.swift",
			".mm" 			: "sourcecode.cpp.objcpp",
			".m" 			: "sourcecode.c.objc",
			".tbd"			: "sourcecode.text-based-dylib-definition",
			".bundle"		: "wrapper.plug-in",
			".a"			: "archive.ar",
			".framework"	: "wrapper.framework",
			".strings"		: "text.plist.strings",
			".applescript"	: "sourcecode.applescript",
			".html"			: "text.html",
			".jpg"			: "image.jpeg",
			".jpeg"			: "image.jpeg",
			".png"			: "image.png",
			".tif"			: "image.tiff",
			".tiff"			: "image.tiff"
		}
		
		if ext in fileTypeMapping :
			fileType = fileTypeMapping [ext]
		else :
			fileType = "text"

		buildPhase = None
		if target != None :
			filePhaseMapping = {
				".c" 			: target.sourcesBuildPhase,
				".cpp" 			: target.sourcesBuildPhase,
				".swift"		: target.sourcesBuildPhase,
				".mm"			: target.sourcesBuildPhase,
				".m"			: target.sourcesBuildPhase,
				".tbd"			: target.frameworkBuildPhase,
				".bundle"		: target.resourceBuildPhase,
				".a"			: target.frameworkBuildPhase,
				".framework"	: target.frameworkBuildPhase,
				".strings"		: target.resourceBuildPhase,
				".applescript"	: target.sourcesBuildPhase,
				".html"			: target.resourceBuildPhase,
				".jpg"			: target.resourceBuildPhase,
				".jpeg"			: target.resourceBuildPhase,
				".png"			: target.resourceBuildPhase,
				".tif"			: target.resourceBuildPhase,
				".tiff"			: target.resourceBuildPhase
			}

			if ext in filePhaseMapping :
				buildPhase = filePhaseMapping [ext]

		fileObj = self.getChild(path, False)
		if fileObj == None:

			# 创建框架文件对象
			info = {}
			info ["path"] = self.helper.converToString(path)
			info ["sourceTree"] = sourceTree
			info ["isa"] = "PBXFileReference"
			info ["lastKnownFileType"] = fileType
			info ["name"] = self.helper.converToString(name)
			fileObj = PBXFileReference(self.helper, self.helper.genObjectId(), info)

			self.addChild(fileObj)

		if buildPhase != None :
			buildPhase.addBuildFile (fileObj, settings)

		return fileObj


# 可变分组，用于实现本地化
class PBXVariantGroup(PBXGroup) :

	def __init__(self, helper, objId, data):
		PBXGroup.__init__(self, helper, objId, data)

	# 添加本地化文件
	# @param path 路径
	# @param lang 语言
	# @param sourceTree 源位置
	# @return 添加后的本地化文件对象
	def addLocalizedFile (self, path, lang, sourceTree = PBXSourceTree.GROUP) :

		if path == None or lang == None :
			return

		localizedFile = self.getChild(path)
		if localizedFile == None :

			# 创建框架文件对象
			localizedInfo = {}
			localizedInfo ["path"] = path
			localizedInfo ["sourceTree"] = sourceTree
			localizedInfo ["isa"] = "PBXFileReference"
			localizedInfo ["lastKnownFileType"] = "text.plist.strings"
			localizedInfo ["name"] = lang
			localizedFile = PBXFileReference(self.helper, self.helper.genObjectId(), localizedInfo)

			self.addChild(localizedFile)

		return localizedFile


# PBXFileReference
class PBXFileReference (PBXNavigatorItem) :

	def __init__(self, helper, objId, data):
		PBXNavigatorItem.__init__(self, helper, objId, data)

	# 获取文件类型
	def getLastKnownFileType(self) :

		if "lastKnownFileType" in self.data :
			return self.helper.getStringValue(self.data["lastKnownFileType"])
		return None

	# 设置文件类型
	def setLastKnownFileType(self, lastKnownFileType):
		self.data["lastKnownFileType"] = lastKnownFileType

	def getIncludeInIndex(self):

		if "includeInIndex" in self.data :
			return self.data["includeInIndex"]
		return None

	def setIncludeInIndex(self, includeInIndex):
		self.data["includeInIndex"] = includeInIndex

	def getExplicitFileType(self):

		if "explicitFileType" in self.data :
			return self.helper.getStringValue(self.data["explicitFileType"])
		return None

	def setExplicitFileType(self, explicitFileType):
		self.data["explicitFileType"] = explicitFileType

# 项目
class PBXProject (PBXObject) :

	def __init__(self, helper, objId, data) :
		PBXObject.__init__(self, helper, objId, data)

		# target
		self.targets = []
		targetIds = self.data["targets"]
		for targetId in targetIds :

			target = self._createTarget(targetId)
			if not target is None:
				self.targets.append(target)

			# targetAttrs = self.data["attributes"]["TargetAttributes"][targetId]
			# self.targets.append(PBXNativeTarget(helper, targetId, helper.root["objects"][targetId], targetAttrs))

		# main group
		mainGroupId = self.data["mainGroup"]
		self.mainGroup = PBXGroup(helper, mainGroupId, helper.root["objects"][mainGroupId])

		# product ref group
		productRefGroupId = self.data["productRefGroup"]
		self.productRefGroup = PBXGroup(helper, productRefGroupId, helper.root["objects"][productRefGroupId])

		# buildConfigurationList
		configListId = self.data["buildConfigurationList"]
		self.buildConfigurationList = XCConfigurationList(helper, configListId, helper.root["objects"][configListId])

	# 创建Target对象
	# @param targetId Target标识
	def _createTarget(self, targetId) :
		
		if not targetId is None :
			obj = self.helper.root["objects"][targetId]
			isa = obj["isa"]

			if isa == "PBXNativeTarget" :

				targetAttrs = None
				if targetId in self.data["attributes"]["TargetAttributes"] :
					targetAttrs = self.data["attributes"]["TargetAttributes"][targetId]

				return PBXNativeTarget(self.helper, self, targetId, obj, targetAttrs)

			elif isa == "PBXAggregateTarget" :
				
				return PBXAggregateTarget(self.helper, self, targetId, obj)

		return None

	# 获取本地化信息
	def getKnownRegions(self) :

		if "knownRegions" in self.data :
			return self.data["knownRegions"]
		return None

	# 设置本地化信息
	def setKnownRegions(self, knownRegions) :
		self.data["knownRegions"] = knownRegions
		
	# 获取开发者本地化信息
	def getDevelopmentRegion(self) :

		if "developmentRegion" in self.data :
			return self.helper.getStringValue(self.data["developmentRegion"])
		return None

	# 设置开发者本地化信息
	def setDevelopmentRegion(self, developmentRegion):
		self.data["developmentRegion"] = developmentRegion

	def getHasScannedForEncodings(self) :

		if "hasScannedForEncodings" in self.data :
			return self.data["hasScannedForEncodings"]
		return None

	def setHasScannedForEncodings(self, hasScannedForEncodings):
		self.data["hasScannedForEncodings"] = hasScannedForEncodings

	def getCompatibilityVersion(self):

		if "compatibilityVersion" in self.data :
			return self.helper.getStringValue(self.data["compatibilityVersion"])
		return None

	def setCompatibilityVersion(self, compatibilityVersion):
		self.data["compatibilityVersion"] = compatibilityVersion

	def getProjectDirPath(self) :

		if "projectDirPath" in self.data :
			return self.helper.getStringValue(self.data["projectDirPath"])
		return None

	def setProjectDirPath(self, projectDirPath):
		self.data["projectDirPath"] = projectDirPath

	def getAttribute(self, name) :

		if "attributes" in self.data :
			return self.data["attributes"][name]
		return None

	def setAttribute(self, name, value):
		self.data["attributes"][name] = value

	# 添加语言区域
	def addRegion(self, region) :
		regions = self.getKnownRegions()
		if region not in regions:
			regions.append(region)
			self.setKnownRegions(regions)

	# 移除语言区域
	def removeRegion(self, region) :
		regions = self.getKnownRegions()
		if region in regions :
			regions.remove(region)
			self.setKnownRegions(regions)


# BuildFile
class PBXBuildFile (PBXObject):

	def __init__(self, helper, objId, data):
		PBXObject.__init__(self, helper, objId, data)

		fileRefId = self.data["fileRef"]
		self.fileRef = PBXFileReference(helper, fileRefId, helper.root["objects"][fileRefId])



# Container Item Proxy
class PBXContainerItemProxy (PBXObject) :

	def __init__(self, helper, project, objId, data):
		PBXObject.__init__(self, helper, objId, data)

		# containerPortal
		if project.objectId == self.data["containerPortal"]:
			self.containerPortal = project

		# proxyType
		self.proxyType = self.data["proxyType"]

		# remoteInfo
		self.remoteInfo = self.data["remoteInfo"]

		# remoteGlobalIDString
		self.remoteGlobalIDString = self.data["remoteGlobalIDString"]


# TargetDependency
class PBXTargetDependency (PBXObject) :

	def __init__(self, helper, project, objId, data) :
		PBXObject.__init__(self, helper, objId, data)

		#target
		targetId = self.data["target"]
		for target in project.targets :
			if target.objectId == targetId :
				self.target = target
				break

		#targetProxy
		targetProxyId = self.data["targetProxy"]
		self.targetProxy = PBXContainerItemProxy(helper, project, targetProxyId, helper.root["objects"][targetProxyId])
		

# Target 基类
class PBXTarget (PBXObject) :

	def __init__(self, helper, project, objId, data):
		PBXObject.__init__(self, helper, objId, data)

		self._buildConfigs = {}

		# dependencies
		self.dependencies = []
		dependencyIds = self.data["dependencies"]
		for dependencyId in dependencyIds :

			dependency = helper.root["objects"][dependencyId]
			dependencyISA = dependency["isa"]
			if dependencyISA == "PBXTargetDependency" :
				# add Dependency
				self.dependencies.append(PBXTargetDependency(helper, project, dependencyId, dependency))


		# Build Phases
		self.buildPhases = []
		buildPhasesIds = self.data["buildPhases"]
		for buildPhasesId in buildPhasesIds:

			buildPhases = helper.root["objects"][buildPhasesId]
			buildPhasesType = buildPhases["isa"]

			buildPhaseObj = None
			if buildPhasesType == "PBXSourcesBuildPhase" :
				self.sourcesBuildPhase = PBXSourcesBuildPhase(helper, buildPhasesId, buildPhases)
				buildPhaseObj = self.sourcesBuildPhase
			elif buildPhasesType == "PBXFrameworksBuildPhase" :
				self.frameworkBuildPhase = PBXFrameworksBuildPhase(helper, buildPhasesId, buildPhases)
				buildPhaseObj = self.frameworkBuildPhase
			elif buildPhasesType == "PBXResourcesBuildPhase" :
				self.resourceBuildPhase = PBXResourcesBuildPhase(helper, buildPhasesId, buildPhases)
				buildPhaseObj = self.resourceBuildPhase
			elif buildPhasesType == "PBXShellScriptBuildPhase" :
				buildPhaseObj = PBXShellScriptBuildPhase(helper, buildPhasesId, buildPhases)
			else :
				buildPhaseObj = PBXBuildPhases(helper, buildPhasesId, buildPhases)

			self.buildPhases.append(buildPhaseObj)

		# Config List
		configListId = self.data["buildConfigurationList"]
		self.buildConfigurationList = XCConfigurationList(helper, configListId, helper.root["objects"][configListId])

	# 获取Target名称
	def getName(self):

		if "name" in self.data :
			return self.helper.getStringValue(self.data["name"])
		return None

	# 设置Target名称
	def setName(self, name):
		self.data["name"] = name


	# 获取产品名称
	def getProductName(self):

		if "productName" in self.data :
			return self.helper.getStringValue(self.data["productName"])
		return None

	# 设置产品名称
	def setProductName(self, productName):
		self.data["productName"] = productName

	# 获取编译配置
	def getBuildConfigs(self, scheme):
		if scheme not in self._buildConfigs :
			for buildConfigs in self.buildConfigurationList.buildConfigurations:
				if buildConfigs.getName() == scheme :
					self._buildConfigs[scheme] = buildConfigs
					break

		return self._buildConfigs[scheme]

	# 获取编译配置
	def getBuildSetting(self, scheme, name):					
		return self.getBuildConfigs(scheme).getBuildSetting(name)

	# 设置编译配置
	def setBuildSetting(self, scheme, name, value):
		self.getBuildConfigs(scheme).setBuildSetting(name, value)

	# 添加Shell脚本编译设置
	def addShellScriptBuildPhase (self, shellScript, path = "/bin/sh") :

		if shellScript == None :
			return

		shellScript = shellScript.replace("\n", "\\n")
		shellScript = shellScript.replace("\"", "\\\"")

		info = {}
		info ["isa"] = "PBXShellScriptBuildPhase"
		info ["buildActionMask"] = self.buildPhases[0].getBuildActionMask()
		info ["files"] = []
		info ["inputPaths"] = []
		info ["outputPaths"] = []
		info ["runOnlyForDeploymentPostprocessing"] = "0"
		info ["shellPath"] = path
		info ["shellScript"] = "\"" + shellScript + "\""

		buildPhase = PBXShellScriptBuildPhase(self.helper, self.helper.genObjectId(), info)
		self.helper.setObject(buildPhase)
		self.buildPhases.append (buildPhase)
		self.data["buildPhases"].append(buildPhase.objectId)


# AggregateTarget
class PBXAggregateTarget (PBXTarget) :

	def __init__(self, helper, project, objId, data):
		PBXTarget.__init__(self, helper, project, objId, data)

# Target
class PBXNativeTarget (PBXTarget) :

	def __init__(self, helper, project, objId, data, targetAttrs) :
		PBXTarget.__init__(self, helper, project, objId, data);

		self._targetAttrs = targetAttrs
		
		# Product Reference
		productRefId = self.data["productReference"]
		self.productReference = PBXFileReference(helper, productRefId, helper.root["objects"][productRefId])


	# 获取产品类型
	def getProductType(self):

		if "productType" in self.data :
			return self.helper.getStringValue(self.data["productType"])
		return None

	# 设置产品类型
	def setProductType(self, productType):
		self.data["productType"] = productType

	# 获取target属性
	def getAttribute(self, name):
		return self._targetAttrs[name]

	# 设置target属性
	def setAttribute(self, name, value):
		self._targetAttrs[name] = value



# BuildPhases
class PBXBuildPhases (PBXObject) :

	def __init__(self, helper, objId, data) :
		PBXObject.__init__(self, helper, objId, data);

		# files
		self.files = []
		for fileId in self.data["files"]:
			self.files.append(PBXBuildFile(helper, fileId, helper.root["objects"][fileId]))

	def getBuildActionMask(self):

		if "buildActionMask" in self.data :
			return self.data["buildActionMask"]
		return None

	def setBuildActionMask(self, buildActionMask):
		self.data["buildActionMask"] = buildActionMask

	def getRunOnlyForDeploymentPostprocessing (self) :

		if "runOnlyForDeploymentPostprocessing" in self.data :
			return self.data["runOnlyForDeploymentPostprocessing"]
		return None

	def setRunOnlyForDeploymentPostprocessing (self, runOnlyForDeploymentPostprocessing) :
		self.data["runOnlyForDeploymentPostprocessing"] = runOnlyForDeploymentPostprocessing

	# 添加编译文件
	# @param fileRef 文件引用对象
	# @param settings 设置信息
	def addBuildFile(self, fileRef, settings = None):

		# 先查找是否已存在该文件引用
		hasExists = False
		for buildFile in self.files :
			if buildFile.fileRef.objectId == fileRef.objectId :
				hasExists = True
				break;

		if not hasExists :
			# 添加编译文件
			buildFileInfo = {}
			buildFileInfo["isa"] = "PBXBuildFile"
			buildFileInfo["fileRef"] = fileRef.objectId
			if settings != None :
				buildFileInfo["settings"] = settings

			buildFile = PBXBuildFile(self.helper, self.helper.genObjectId(), buildFileInfo)
			self.files.append(buildFile)
			self.helper.setObject(buildFile)

			self.data["files"].append(buildFile.objectId)

	# 移除编译文件
	# @param fileRef 文件引用对象
	def removeBuildFile(self, fileRef):

		needsDelBuildFiles = []
		for buildFile in self.files:
			if buildFile.fileRef.objectId == fileRef.objectId:
				needsDelBuildFiles.append(buildFile)

		for buildFile in needsDelBuildFiles:
			self.files.remove(buildFile)
			self.data["files"].remove(buildFile.objectId)
			self.helper.delObject(buildFile)



# Sources Build Phases
class PBXSourcesBuildPhase(PBXBuildPhases):

	def __init__(self, helper, objId, data) :
		PBXBuildPhases.__init__(self, helper, objId, data);

# Framework Build Phases
class PBXFrameworksBuildPhase(PBXBuildPhases):

	def __init__(self, helper, objId, data) :
		PBXBuildPhases.__init__(self, helper, objId, data);
		
# Resource Build Phases
class PBXResourcesBuildPhase(PBXBuildPhases):
	
	def __init__(self, helper, objId, data) :
		PBXBuildPhases.__init__(self, helper, objId, data);

class PBXShellScriptBuildPhase(PBXBuildPhases):

	def __init__(self, helper, objId, data) :
		PBXBuildPhases.__init__(self, helper, objId, data);

	# 获取脚本路径
	def getShellPath(self):
		if "shellPath" in self.data :
			return self.helper.getStringValue(self.data["shellPath"])
		return None

	# 设置脚本路径
	def setShellPath(self, shellPath):
		self.data["shellPath"] = shellPath

	# 获取脚本内容
	def getShellScript(self):

		if "shellScript" in self.data :
			return self.helper.getStringValue(self.data["shellScript"])
		return None

	# 设置脚本内容
	def setShellScript(self, shellScript):
		self.data["shellScript"] = shellScript
		



# python PBXProjectHelper.py /Users/fenghj/Documents/work/Demo/Demo.xcodeproj/project.pbxproj
# def main():

# 	sys.setdefaultencoding('utf-8')

# 	if  len (sys.argv) > 1 :
# 		pbxPath = sys.argv[1]
# 		parser = PBXProjectHelper (pbxPath)

		# parser.project.mainGroup.addFile("test/AppDelegate+Demo.m", parser.project.targets[0])
		# parser.project.mainGroup.addFile("test/AppDelegate+Demo.mm", parser.project.targets[0])
		# parser.project.mainGroup.addFile("test/test.swift", parser.project.targets[0])

		# parser.project.addRegion("zh-Hans")
		# parser.project.removeRegion("zh-Hans")

		# for target in parser.project.targets:
		# 	print "target(%s) = %s" %(target.getISA(), target.getName())


		# target = parser.project.mainGroup.find("/MobPods/Demo11")
		# print "group = %s" %(target)
		# group = parser.project.mainGroup.find("/MobPods/Demo11/YYImage")
		# print "group = %s" %(group)
		# target.removeChild(group)

		# parser.project.mainGroup.find("/demo1").removeChild(group)

		# demo1Group = parser.project.mainGroup.find("/demo1")
		# group = demo1Group.addGroup("xxx1")
		# group = group.addGroup("xxx1")
		# group = group.addGroup("xxx2")
		# group = group.addGroup("xxx3")

		# xxxGroup = parser.project.mainGroup.find("/demo1/xxx")
		# demo1Group.removeChild(xxxGroup)

		# frameworkGroup = parser.project.mainGroup.find("Demo")
		# frameworkGroup.addStaticLib("libLuaScriptCore.a", parser.project.targets[0])
		# frameworkGroup.addSystemDylib("libz.tbd", parser.project.targets[0])
		# frameworkGroup.addSystemFramework("AVFoundation.framework", parser.project.targets[0], False)

		# avfoundationFile = parser.project.mainGroup.find("/Frameworks/AVFoundation.framework")
		# frameworkGroup.removeChild(avfoundationFile)

		# libzFile = parser.project.mainGroup.find("/Frameworks/libz.tbd")
		# frameworkGroup.removeChild(libzFile)

		# lscFile = parser.project.mainGroup.find("/Frameworks/libLuaScriptCore.a")
		# frameworkGroup.removeChild(lscFile)

		# demo1Group.addHeaderFile("../LuaScriptCore.h")

		# headerFile = parser.project.mainGroup.find("/demo1/LuaScriptCore.h")
		# demo1Group.removeChild(headerFile)

		# bundleFile = demo1Group.addBundle("../ShareSDK.bundle", parser.project.targets[0])
		# demo1Group.removeChild(bundleFile)

		# debugConfigs = parser.project.targets[0].getBuildConfigs("Debug")
		# debugConfigs.addFrameworkSearchPath("demo/frameworks")
		# debugConfigs.addLibrarySearchPath("xxx/xxx1")
		# debugConfigs.addOtherLinkerFlag("test")

		# testGroup = parser.project.mainGroup.find("/test")
		# testGroup.addLocalizedFile("Base.lproj/aa.strings", "Base", parser.project.targets[0])
		# testGroup.addLocalizedFile("en.lproj/aa.strings", "en", parser.project.targets[0])

		# localizedGroup = parser.project.mainGroup.find("/test/aa.strings")
		# if localizedGroup != None :
		# 	testGroup = parser.project.mainGroup.find("/test")
		# 	testGroup.removeChild(localizedGroup)

		# parser.project.targets[0].addShellScriptBuildPhase("echo \"xxxGroup\"\necho 111");
# 		parser.save()


# if __name__ == "__main__":
# 	sys.exit(main())