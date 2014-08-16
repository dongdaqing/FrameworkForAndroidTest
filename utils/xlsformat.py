# -*- coding: utf-8 -*-
'''
Created on 2014-2-27

@author: meng
'''
import os,time,codecs
from pyExcelerator import *


class XlsFormat(object):
    def __init__(self):
        
        #set borders
        self.borders = Borders()
        self.borders.left   = self.borders.THIN
        self.borders.right   = self.borders.THIN
        self.borders.top  = self.borders.THIN
        self.borders.bottom   = self.borders.THIN

        #set alignment
        self.alignment = Alignment()
        self.alignment.horz = self.alignment.HORZ_CENTER
        self.alignment.vert = self.alignment.VERT_CENTER

        #set font to bold
        self.font = Font() # Create the Font
        self.font.name = 'Times New Roman'
        self.font.bold = True
        self.font.height = 0x00C8+50


        #green
        self.style_green = XFStyle()
        self.pattern = Pattern()
        self.pattern.pattern_back_colour = 0x0b
        self.pattern.pattern_fore_colour = 0x0b
        self.pattern.pattern = self.pattern.SOLID_PATTERN
        self.style_green.pattern = self.pattern
        self.style_green.borders = self.borders

        #red
        self.style_red = XFStyle()
        self.pattern = Pattern()
        self.pattern.pattern_back_colour = 0x0a
        self.pattern.pattern_fore_colour = 0x0a
        self.pattern.pattern = self.pattern.SOLID_PATTERN
        self.style_red.pattern = self.pattern
        self.style_red.borders = self.borders

        #title to purple
        self.style_title = XFStyle()
        self.pattern = Pattern()
        self.pattern.pattern_back_colour = 0x0F
        self.pattern.pattern_fore_colour = 0x0F
        self.pattern.pattern = self.pattern.SOLID_PATTERN
        self.style_title.pattern = self.pattern
        self.style_title.borders = self.borders

        #subtitle to bold
        self.style_subtitle = XFStyle()
        self.style_subtitle.borders = self.borders
        self.style_subtitle.font = self.font

        #custom
        self.style_custom = XFStyle()
        self.style_custom.borders = self.borders

