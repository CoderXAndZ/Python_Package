# Python_Package
使用Python打多个企业包，动态修改企业包plist中的文件，实现一包多用的功能
Python打企业包：实现自动读取Excel表格中数据，动态往ipa的plist中的添加值，重新签名等

0、Xcode编译、重新签名、打包和导出功能的实现；
1、界面上的4个路径都需要选择，当少选择路径直接点击开始打包时，给弹框提示，直到4个路径全部选择完毕才可以开始打包；
2、每次得到推荐人Excel之后，根据推荐人Excel内容，替换掉Xcode中旧版本的plist；
3、打包成功的ipa的文件名的修改，将所有的rzjrapp.ipa包命名为(app+userid).ipa；
4、打包成功之后退出页面；
5、打包成功进行弹窗提示，打包成功后，点击确定，打开IPA包所在的文件夹；
6、实现界面化的选择excel路径，并将excel中的第一个sheet的第一列数据转换成打包文件的列表，直接读取Excel表格，不需要再手动输入推荐人的userid；
7、将所有的重命名之后的IPA包统一存放，并删除所有的打包文件；
8、在ipa同一存放的文件夹中创建每一个ipa对应的plist文件；
9、修改Xcode版本就行打包：这个得是基于电脑上有多个版本才可以，如果没有依旧不能实现；
10、实现界面化的选择工程路径和ipa的输出路径
11、输出路径可以不选择，如果不选择，默认在桌面创建“生成的ipa包”文件夹存放打包好的ipa包和对应的plist；
12、自动在存放ipa包的文件夹创建DistributionSummary.plist和ExportOptions.plist；

注意：
1>如果不在ExportOptions.plist中添加provisioningProfiles字典的话是没有办法打包成功的；
2>如果上线版和企业版不是一个Team的话，当打企业包的时候，还是需要在Xcode上填写企业版的BundleID，选择企业版的Team才可以，否则打包不成功；

