# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import genapk,youkutestcases,multithreadcls,logcatrecorder
from utils import sendemail
from performance import performance
import time,os,platform

class StartTest(object):

    def __init__(self,deviceid):
        #生成记录日志路径
        sys_info = platform.system()
        if sys_info == "Windows":
            common_test_path = r"D:\svn\repos\AutomatedTesting\Android\FrameworkForAndroidTest\uitest\temp"
            common_testsvn_path = r"D:\svn\repos"
            temp_path = r"D:\temp"
        elif sys_info == "Linux":
            common_test_path = ""
            common_testsvn_path = ""
            temp_path = ""
        else:
            common_test_path = r"/Users/dongdaqing/temp"
            common_testsvn_path = r"/Users/dongdaqing/SVN/MobileTest"
            temp_path = r""

        #生成记录日志路径
        self.time_as_path = time.strftime('%Y%m%d%H%M%S',time.localtime())
        self.rootpath = os.path.join(common_test_path,self.time_as_path)
        if not os.path.exists(self.rootpath):
            os.mkdir(self.rootpath)

        #截图临时存放路径
        self.temp_path=temp_path
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)
        
        #测试用例位置
        self.func_name_path = os.path.join(common_testsvn_path,r"AutomatedTesting/Android/Robotium/branches/YoukuMobileTest_3.1/src/com/youku/phone/test")
        if sys_info == "Windows":
            self.rootpath = self.rootpath.replace("/",os.sep)
            self.func_name_path = self.func_name_path.replace("/",os.sep)
        elif sys_info == "Linux":
            self.rootpath = ""
            self.func_name_path = ""
        else:
            self.rootpath = self.rootpath.replace("\\",os.sep)
            self.func_name_path = self.func_name_path.replace("\\",os.sep)
        #测试过程日志记录
        self.running_file = os.path.join(self.rootpath,'TestResult.txt')
        #Android日志记录
        self.logcatfile = os.path.join(self.rootpath,'logcatfile.txt')
        #性能数据记录
        self.performancefile = os.path.join(self.rootpath,'performancefile.txt')
        #测试用例测试结果记录
        self.caseresult_filename = os.path.join(self.rootpath,'caseresult.txt')
        #image_test传入deviceid参数
        self.deviceid=deviceid

    def prepareTest(self):
        #执行打包函数
        genapk.GenAPK(self.running_file).genApk()

    def testcasesThread(self):
        #执行测试用例
        youkutestcases.YoukuTestCases(self.running_file,self.caseresult_filename,self.func_name_path,self.temp_path,self.deviceid).execTestCases()

    def performanceThread(self):
        #性能数据收集
        performance.Performance(self.performancefile).collectPerformance()

    def logcatThread(self):
        #logcat日志收集
        logcatrecorder.LogcatRecorder(self.logcatfile).startLogcat()

    def collect_thread(self):
        thread1 = multithreadcls.StartTestMultiThread(self.testcasesThread)
        thread2 = multithreadcls.StartTestMultiThread(self.performanceThread)
        thread3 = multithreadcls.StartTestMultiThread(self.logcatThread)

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        #线程一直停止不掉，不将此线程挂起
#        thread3.join()

    def sendmailresult(self):
        #将测试结果以邮件发出
        sendemail.SendEmail(self.running_file).begintosend()
    

if __name__=='__main__':
    startTest_obj = StartTest()
    startTest_obj.prepareTest()
    startTest_obj.collect_thread()
    startTest_obj.sendmailresult()