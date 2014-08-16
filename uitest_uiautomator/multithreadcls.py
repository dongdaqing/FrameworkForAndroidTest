# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import time,os,threading

class StartTestMultiThread(threading.Thread):

    def __init__(self,func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        apply(self.func)