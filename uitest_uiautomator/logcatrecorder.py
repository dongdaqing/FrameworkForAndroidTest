# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import os

class LogcatRecorder(object):
    def __init__(self,filename):
        self.file_name = filename

    def startLogcat(self):
        os.system('adb shell logcat >> %s'%self.file_name)

if __name__=='__main__':

    # logcat_obj=LogcatRecorder(file_name)
    # logcat_obj.startLogcat()
    pass
