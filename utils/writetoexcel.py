# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import os,time,codecs
from pyExcelerator import *

class WritetoExcel(object):
    def __init__(self,filename):
        self.root_path = os.path.dirname(filename)

        #设置边框
        borders = Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1

        #水平向左，垂直居中对齐
        al1 = Alignment()
        al1.horz = Alignment.HORZ_LEFT
        al1.vert = Alignment.VERT_CENTER
        al1.wrap = Alignment.WRAP_AT_RIGHT

        #excel颜色定义
        #绿色
        self.style_green = XFStyle()
        self.pattern = Pattern()
        self.pattern.pattern_back_colour = 0x11
        self.pattern.pattern_fore_colour = 0x11
        self.pattern.pattern = self.pattern.SOLID_PATTERN
        self.style_green.pattern = self.pattern

        #红色
        self.style_red = XFStyle()
        self.pattern = Pattern()
        self.pattern.pattern_back_colour = 0x0a
        self.pattern.pattern_fore_colour = 0x0a
        self.pattern.pattern = self.pattern.SOLID_PATTERN
        self.style_red.pattern = self.pattern

        #普通
        self.style_basic = XFStyle()
        self.style_basic.alignment = al1
        self.style_basic.borders = borders

    def txtToExcel(self,flag):
        """
        将txt文件写入excel
        """
        root_path = self.root_path
        assert os.path.exists(root_path)
        w=Workbook()
        os.chdir(root_path)

        file_names = os.listdir('.')
        for file_name in file_names:
            if file_name.find(flag) != -1:
                file_path = os.path.join(root_path,file_name)
                ws = w.add_sheet(flag)
                try:
                    f = codecs.open(file_path,'r','utf-8')
                except IOError:
                    sys.exit('Failed to open')
                else:
                    lines = f.readlines()
                finally:
                    f.close()
                for i in range(0,len(lines)):
                    line = lines[i].split('\t')
                    for j in range(0,len(line)):
                        b=line[j].strip()
                        if b == 'Failed':
                            ws.write(i,j,b,self.style_red)
                        elif b == 'Passed':
                            ws.write(i,j,b,self.style_green)
                        else:
                            ws.write(i,j,b)
        save_path=os.path.join(root_path,flag+'.xls')
        if os.path.exists(save_path):
            os.remove(save_path)
        w.save(save_path)

    def basicToExcel(self,ws,row,col,src):
        """
        将dict，str写入excel
        """
        ws.write(row,col,src,self.style_basic)



if __name__ == '__main__':
    filename = 'D:\\svn\\repos\\AutomatedTesting\\DailyBuild\\uitest\\temp\\20130701175043\\caseresult.txt'
    WritetoExcel(filename).txtToExcel('caseresult')
