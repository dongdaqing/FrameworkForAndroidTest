# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import subprocess,os,time
import logging
import readsourcefile
from utils import loggingmodule,writetoexcel,image_process
from pyExcelerator import *
import platform
import zipfile,json

class YoukuTestCases(object):

    def __init__(self,filename,caseresult_filename,funcname_path,temp_path,deviceid):
        u"""initial logger"""
        self.logger = loggingmodule.Logger('youkutestcases',filename)
        self.logger_caseresult = loggingmodule.Logger('casereslut',caseresult_filename)
        self.funcname_path = funcname_path
        self.readfile_obj = readsourcefile.ReadSourceFile()
        self.testcase_loop = 3
        self.filename = filename
        self.root_path = os.path.dirname(filename)
        #Robotium-Screenshots压缩包的存放路径
        self.screenshots_file = os.path.join(self.root_path,r"Robotium-Screenshots.zip")
        #Robotium-Screenshots存放在文件夹下
        self.screenshots_file2 = os.path.join(self.root_path,r"screenshots")
        if not os.path.exists(self.screenshots_file2):
            os.mkdir(self.screenshots_file2)
        self.temp_path = temp_path
        self.deviceid=deviceid

    def installAPK(self):
        """
        卸载、安装应用
        """
        #判断当前手机是否安装应用
        return_info = os.popen('adb -s %s shell am start -n com.youku.phone/com.youku.phone.ActivityWelcome'%(self.deviceid)).read()
        self.logger.log(return_info)

        if return_info.find('Error type 3') != -1:
            installInfo = os.popen('adb -s %s install Youku_Android_ForTest.apk'%(self.deviceid)).read()
            self.logger.log(installInfo)
            time.sleep(2)
        else:
            uninstallInfo = os.popen('adb -s %s uninstall com.youku.phone'%(self.deviceid)).read()
            self.logger.log(uninstallInfo)
#            uninstallInfo2 = os.popen('adb uninstall com.youku.phone.test').read()
#            self.logger.log(uninstallInfo2)
            time.sleep(2)
            installInfo = os.popen('adb -s %s install Youku_Android_ForTest.apk'%(self.deviceid)).read()
            self.logger.log(installInfo)
            time.sleep(2)


    def runAllTestCases(self):
        """
        执行所有测试用例
        """
        resultInfo = os.popen('adb shell am instrument -e class com.youku.phone.test.SearchActivityTest\
                                    -w com.youku.phone.test/android.test.InstrumentationTestRunner').read()
        self.logger.log(resultInfo)

    def writeDeviceInfo(self):
        """
        写入设备信息
        """
        self.logger_caseresult.log('%s\t%s\t%s\t%s'%('Brand','Model','AndroidSystem','Density'))
        device_info = self.readfile_obj.parseDeviceInfo(self.deviceid)
        self.logger_caseresult.log('%s\t%s\t%s\t%s'%(device_info[0],device_info[1],device_info[2],device_info[3]))
        self.logger_caseresult.log('%s'%(' '))
    def runSingleTestCase(self):
        """
        单独执行每个测试用例
        """
        #写入设备信息
        self.writeDeviceInfo()
        #测试用例结果样式
        self.logger_caseresult.log('%s\t%s\t%s\t%s\t%s\t%s\t%s'%('Time','Module','TestCases','CaseDescription','AppVer','TestResults','DetailInfo'))
        os.chdir(self.funcname_path)
        file_list = os.listdir('.')
        for file in file_list:
            #获取文件名
            file_name = self.readfile_obj.parseJavaFile(file)
            #获取该文件的函数名
            func_list = self.readfile_obj.parseFunction(file)
            func_info = self.readfile_obj.parseFunctioninfo(file)
            #用于测试，单独执行SearchActivity
#            if file_name == 'ProfileActivityTest':
#                for i in range(0,len(func_list),1):
#                    detail_info = ''
#                    resultInfo = os.popen('adb shell am instrument -e class com.youku.phone.test.{0}#{1}\
#                                -w com.youku/android.test.InstrumentationTestRunner'.format(file_name,func_list[i])).read()
#                    if (resultInfo.find('AssertionFailedError') != -1) or (resultInfo.find('shortMsg=Process crashed') != -1)\
#                                            or (resultInfo.find('Failure') != -1):
#                        test_result = 'Failed'
#                        detail_info = self.readfile_obj.parseDetailInfo(resultInfo)
#                    else:
#                        test_result = 'Passed'
#                    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
#                    self.logger.log('%s\t%s'%(cur_time,resultInfo))
#                    self.logger_caseresult.log('%s\t%s\t%s\t%s\t%s\t%s\t%s'%(cur_time,file_name,func_list[i],func_info[i],'v3.1',test_result,detail_info))
#                    break

            #正式方法
            for i in range(0,len(func_list),1):
                for j in range(0,self.testcase_loop,1):
                    #测试用例失败详细信息
                    detail_info = ''
                    #错误测试用例内容去重
                    isWrited = 0
                    resultInfo = os.popen('adb -s %s shell am instrument -e class com.youku.phone.test.{0}#{1}\
                                    -w com.youku/android.test.InstrumentationTestRunner'.format(file_name,func_list[i])%(self.deviceid)).read()

                    if (resultInfo.find('AssertionFailedError') != -1) or (resultInfo.find('shortMsg=Process crashed') != -1)\
                        or (resultInfo.find('Failure') != -1):
                        #当前测试用例执行失败，循环继续执行
                        cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                        test_result = 'Failed'
                        detail_info = self.readfile_obj.parseDetailInfo(resultInfo)
                        self.logger_caseresult.log('%s\t%s\t%s\t%s\t%s\t%s\t%s'%(cur_time,file_name,func_list[i],func_info[i],'v3.1',test_result,detail_info))
                        self.logger.log('%s\t%s'%(cur_time,resultInfo))
                        continue
                    else:
                        #测试用例返回信息没有发现错误，退出当前测试用例
                        cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                        test_result = 'Passed'
                        self.logger_caseresult.log('%s\t%s\t%s\t%s\t%s\t%s\t%s'%(cur_time,file_name,func_list[i],func_info[i],'v3.1',test_result,detail_info))
                        self.logger.log('%s\t%s'%(cur_time,resultInfo))
                        break

    def collectScreenshots(self):
        #将Robotium截图pull到存放测试结果的路径,并压缩打包
        os.system('adb -s %s pull /sdcard/Robotium-Screenshots %s'%(self.deviceid,self.temp_path))
        z = zipfile.ZipFile(self.screenshots_file, 'w')
        if os.path.isdir(self.temp_path):
            for d in os.listdir(self.temp_path):
                z.write(self.temp_path+os.sep+d)
        z.close()
        for file in os.listdir(self.temp_path):
            delFile=os.path.join(self.temp_path,file)
            if os.path.isfile(delFile):
                os.remove(delFile)
    def pullScreenshots(self):
        #将Robotium截图pull到存放测试结果的路经文件夹下，不压缩
        os.system('adb -s %s pull /sdcard/Robotium-Screenshots %s'%(self.deviceid,self.screenshots_file2))
        
    def execTestCases(self):
#        self.installAPK()
        #防止测试用例执行失败后，没有将完成的写到excel里面
        try:
            self.runSingleTestCase()
#            self.collectScreenshots()
            self.pullScreenshots()
        except:
            writetoexcel.WritetoExcel(self.filename).txtToExcel('caseresult')
        else:
            writetoexcel.WritetoExcel(self.filename).txtToExcel('caseresult')

if __name__=='__main__':
    test=YoukuTestCases()
    test.execTestCases()