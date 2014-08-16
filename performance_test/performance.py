# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

from utils import loggingmodule,writetoexcel
import os,time
from pyExcelerator import *


class Performance(object):

    def __init__(self,filename):
        self.logger = loggingmodule.Logger('performance',filename)
        self.root_path = os.path.dirname(filename)
        self.filename = filename

    def getCpuVssRss(self,app):
        """
        Parse adb shell top
        """
        cpu = '0%'
        vss = '0'
        rss = '0'
        systemOutput = os.popen('adb shell top -m 10 -n 1 -d 1 -m 12').read()
        systemInfo = systemOutput.split('\n')
        for app_info in systemInfo:
            if app_info.find(app) != -1 and \
            app_info.find('com.youku.phone:push') == -1 and \
            app_info.find('com.youku.phone:download') == -1 and \
            app_info.find('com.youku.phone:GameCenterDownloadService') == -1:
                app_info_detail = app_info.split(' ')
                for cpu_info in app_info_detail:
                    if cpu_info.find('%') != -1:
                        cpu = cpu_info
                        break
                for vss_info in app_info_detail:
                    if vss_info.find('K') != -1:
                        index_v = vss_info.find('K')
                        vss = int(vss_info.strip()[:index_v])/1024
                        break
                for rss_info in range(len(app_info_detail)-1,-1,-1):
                    if app_info_detail[rss_info].find('K') != -1:
                        index_r = app_info_detail[rss_info].find('K')
                        rss = int(app_info_detail[rss_info].strip()[:index_r])/1024
                        break
        return (cpu,vss,rss,app)

    def writeToFile(self,app='com.youku.phone',totalcount=25):
        """
        将分析数据写入txt文件
        """
        currnum=0
        self.logger.log('%s\t%s\t%s\t%s\t'%('TIME','CPU','VSS(MB)','RSS(MB)'))
        while currnum < totalcount:
            cur_info = self.getCpuVssRss(app)
            index = cur_info[0].strip().find('%')
            cpu = int(cur_info[0].strip()[:index])
            if cur_info[0] == '0%':
                currnum = currnum + 1
                print currnum
            elif cpu > 100:
                pass
            else:
                cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                self.logger.log('%s\t%s\t%s\t%s\t'%(cur_time,cur_info[0],cur_info[1],cur_info[2]))
                #重置计数器
                currnum = 0

    def collectPerformance(self):
        self.writeToFile()
        writetoexcel.WritetoExcel(self.filename).txtToExcel('performance')

if __name__ == '__main__':
    time_as_path = time.strftime('%Y%m%d%H%M%S',time.localtime())
    rootpath = os.path.join(r'e:\temp',time_as_path)
    if not os.path.exists(rootpath):
        os.mkdir(rootpath)

    performancefile = os.path.join(rootpath,'performancefile.txt')

    per_obj = Performance(performancefile).collectPerformance()
