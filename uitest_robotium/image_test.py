# -*- coding: utf-8 -*-
'''
Created on 2014-3-25
@description:借助PIL，利用图片相似度实现UI测试自动化；
             ref：http://blog.csdn.net/gzlaiyonghao/article/details/2325027
@author: meng
'''
import starttest,readsourcefile
from utils import image_process,xlsformat
import zipfile
import os
from pyExcelerator import *
class ImageTest(object):
    def __init__(self):
        self.deviceid1='02def475'#mi1
        self.deviceid2='3633D590283400EC'#nexus s
        #获取设备信息
        self.readfile_obj = readsourcefile.ReadSourceFile()
        device_info1 = self.readfile_obj.parseDeviceInfo(self.deviceid1)
        deviceinforesult1=device_info1[0]+device_info1[1]
        
        device_info2 = self.readfile_obj.parseDeviceInfo(self.deviceid2)
        deviceinforesult2=device_info2[0]+device_info2[1]
        
        self.sheet_title=['num',deviceinforesult1,deviceinforesult2,'cmp_result']
        self.filename=r'image_process.xls'
        self.w = Workbook()
        #ws该sheet写入图片对比的结果
        self.ws = self.w.add_sheet("image_process")
        #设置列宽
        self.ws.col(1).width = 0x0d00 + 9000
        self.ws.col(2).width = 0x0d00 + 9000
        self.ws.col(3).width = 0x0d00 + 6000
        #sheet写入子标题
        #xls的格式
        self.xmlformat = xlsformat.XlsFormat()
        for i in range(len(self.sheet_title)):
            self.ws.write(0,i,self.sheet_title[i],self.xmlformat.style_title)
        
    def start(self):
        test_obj1=starttest.StartTest(self.deviceid1)
        test_obj1.testcasesThread()
        screenshots1=os.path.join(test_obj1.rootpath,r"Screenshots")
        
        test_obj2=starttest.StartTest(self.deviceid2)
        test_obj2.testcasesThread()
        screenshots2=os.path.join(test_obj2.rootpath,r"Screenshots")
        
        os.chdir(screenshots1)
        file_list=os.listdir('.')
        row_n=1
        for file_item in file_list:
            file1 = os.path.join(screenshots1,file_item)
            file2 = os.path.join(screenshots2,file_item)

            if os.path.exists(file2) and os.path.exists(file1):
                result=image_process.ImageProcess().calc_similar_by_path(file1, file2)*100
                print 'test_case: %.3f%%'%(result)
                self.ws.write(row_n,0,row_n,self.xmlformat.style_custom)
                self.ws.write(row_n,1,file_item,self.xmlformat.style_custom)
                self.ws.write(row_n,2,file_item,self.xmlformat.style_custom)
                self.ws.write(row_n,3,str(result)+'%',self.xmlformat.style_custom)
                row_n+=1
            else:
                self.ws.write(row_n,0,row_n,self.xmlformat.style_custom)
                self.ws.write(row_n,1,file_item,self.xmlformat.style_custom)
                self.ws.write(row_n,3,'file missed!',self.xmlformat.style_red)
                row_n+=1
        save_filename=os.path.join(os.path.dirname(test_obj1.rootpath),self.filename)
        self.w.save(save_filename)
if __name__=='__main__':
    image_test_obj=ImageTest()
    image_test_obj.start()
    