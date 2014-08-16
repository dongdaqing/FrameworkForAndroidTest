# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import time,logging,os

class Logger(object):

    def __init__(self,logName,logFile):
        #log纪录定义
        self.logger = logging.getLogger(logName)
        self.logger.setLevel(logging.DEBUG)
        #定义日志输出到文件的handler
        inputFile = logging.FileHandler(logFile)
        inputFile.setLevel(logging.DEBUG)
        #定义日志输出到控制台的handler
        inputConsole = logging.StreamHandler()
        inputConsole.setLevel(logging.DEBUG)
        #添加handler
        self.logger.addHandler(inputFile)
        self.logger.addHandler(inputConsole)

    def log(self,msg):
        """
        封装info函数
        """
        if self.logger is not None:
            self.logger.info(msg)