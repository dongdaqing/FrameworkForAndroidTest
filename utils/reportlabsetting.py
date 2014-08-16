# -*- coding: utf-8 -*-
'''
Created on 2014-2-28

@author: meng
'''
import os
import xlrd
from reportlab.lib import colors  
from urllib import urlopen  
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import *  
from reportlab.graphics.charts.lineplots import LinePlot  
from reportlab.graphics import renderPDF
class ReportlabSetting(object):
    #title:图的名称，ylable：y轴注释
    def __init__(self,title,ylable):
        self.drawing = Drawing(400,200)   
        self.lp = LinePlot()  
        self.lp.x = 50  
        self.lp.y = 50  
        self.lp.height = 125  
        self.lp.width = 300
        #title设置
        self.title = Label()
        self.title.fontSize   = 12
        title_text = title
        self.title._text = title_text
        self.title.x          = 190
        self.title.y          = 190
        self.title.textAnchor ='middle'
        #x轴设置
        self.Xlabel = Label()
        self.Xlabel._text = 'time'
        self.Xlabel.fontSize   = 12
        self.Xlabel.x          = 380
        self.Xlabel.y          = 30
        self.Xlabel.textAnchor ='middle'
        #y轴设置
        self.Ylabel = Label()
        self.Ylabel._text = ylable
        self.Ylabel.fontSize   = 12
        self.Ylabel.x          = 40
        self.Ylabel.y          = 190
        self.Ylabel.textAnchor ='middle'
    #filename：pdf文件输出名
    def drawline(self,time_axis,para,filename):
        self.lp.data = [zip(time_axis,para)]
        self.drawing.add(self.lp)  
        self.drawing.add(self.title)
        self.drawing.add(self.Xlabel)
        self.drawing.add(self.Ylabel)
        renderPDF.drawToFile(self.drawing,filename,'Sunspots')