# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import os,platform

func_path = 'D:\\svn\\repos\\AutomatedTesting\\Android\\Robotium\\branches\\YoukuMobileTest_3.1\\src\\com\\youku\\phone\\test'

#func_path = '/Users/dongdaqing/SVN/MobileTest/AutomatedTesting/Android/Robotium/branches/YoukuMobileTest_3.1/src/com/youku/phone/test'
#str_info = '/Users/dongdaqing/temp/TestResult.txt'

class ReadSourceFile(object):

    def __init__(self,):
        pass

    def parseFunction(self,source_filename):

        func_list=[]
        f = open(source_filename,'r')
        read_line = f.read()
        for line in read_line.split('\n'):
            if line.find('test') != -1:
                func_def = line.split(' ')
                for func_name in func_def:
                    if func_name.find('()') != -1:
                        index = func_name.find('()')
                        testcase = func_name[:index]
                        func_list.append(testcase)
        return func_list

    def parseFunctioninfo(self,source_filename):

        func_info=[]
        f = open(source_filename,'r')
        read_line = f.read()
        for line in read_line.split('\n'):
            if line.find('Description') != -1:
                func_def = line.split(' ')
                for func_name in func_def:
                    if func_name.find(':') != -1:
                        index = func_name.find(':')
                        testdes = func_name[index+1:]
                        func_info.append(testdes)
        return func_info

    def parseJavaFile(self,java_file):
        file_name = java_file.split('.')
        return file_name[0].strip()

    def parseDetailInfo(self,str_result):
        detail_info_list = str_result.split('\n')
        for detail_info in detail_info_list:
            if detail_info.find('AssertionFailedError') != -1:
                return detail_info.strip()
            elif detail_info.find('Process crashed') != -1:
                index = detail_info.find('=')
                return detail_info[(index+1):].strip()

    def parseDeviceInfo(self,deviceid):

        brand = ''
        model = ''
        version = ''
        density = ''
        sys_info = platform.system()
        if sys_info == "Windows":
            adbDensityInfo = os.popen('adb -s %s shell getprop | find "density"'%(deviceid)).read()
        elif sys_info == "Linux":
            adbDensityInfo = os.popen('adb -s %s shell getprop | grep "density"'%(deviceid)).read()
        else:
            adbDensityInfo = os.popen('adb -s %s getprop | grep "density"'%(deviceid)).read()
        densityInfo_detail = adbDensityInfo.split(' ')
        for density_info in range(len(densityInfo_detail)-1,-1,-1):
            if densityInfo_detail[density_info].find('[') != -1:
                    index_d = densityInfo_detail[density_info].find(']')
                    density = densityInfo_detail[density_info].strip()[1:index_d]
                    break
        adbDeviceInfo = os.popen('adb -s %s shell cat /system/build.prop'%(deviceid)).read()
        deviceInfo = adbDeviceInfo.split('\n')
        for i in range(0,len(deviceInfo)):
            device_info_detail = deviceInfo[i]
            if device_info_detail.find('brand') != -1:
                    index_b = device_info_detail.find('=')
                    brand = device_info_detail.strip()[index_b+1:]
                        
            if device_info_detail.find('model') != -1:
                    index_m = device_info_detail.find('=')
                    model = device_info_detail.strip()[index_m+1:]

            if device_info_detail.find('build.version.release') != -1:
                    index_v = device_info_detail.find('=')
                    version = device_info_detail.strip()[index_v+1:]   
        return (brand,model,version,density)
#测试函数
if __name__ == '__main__':
    func_obj = ReadSourceFile()
#    os.chdir(func_path)
#    file_list = os.listdir('.')
#    for file in file_list:
#        file_name = func_obj.parseJavaFile(file)
#        if file_name == 'SearchActivityTest':
#            func_list = func_obj.parseFunction(file)
#            for i in range(0,len(func_list),1):
#                print file_name,func_list[i]
#                os.system('adb shell am instrument -e class com.youku.phone.test.{0}#{1}\
#                     -w com.youku.phone.test/android.test.InstrumentationTestRunner'.format(file_name,func_list[i]))

    resultInfo = os.popen('adb shell am instrument -e class com.youku.phone.test.SearchActivityTest#testEnterSearch\
                     -w com.youku.phone.test/android.test.InstrumentationTestRunner').read()
    detail_info = func_obj.parseDetailInfo(resultInfo)
    print detail_info