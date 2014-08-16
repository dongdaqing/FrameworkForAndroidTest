# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import os,time
import deploy,logcatrecorder,multithreadcls

class StartTest(object):

    def __init__(self):
        doc_path = os.path.join(os.path.dirname(__file__),'doc')
        test_results = os.path.join(doc_path,'test_results')
        if not os.path.exists(test_results):
            os.mkdir(test_results)
        time_as_path = time.strftime('%Y%m%d%H%M%S', time.localtime())
        root_path = os.path.join(test_results, time_as_path)
        if not os.path.exists(root_path):
            os.mkdir(root_path)

        self.logcat_file = os.path.join(root_path, 'logcat_file.txt')
        self.uiautomator_test_results = os.path.join(root_path, 'uiautomator_test_results.txt')

    def testcase_thread(self):
        deploy.Deploy(self.uiautomator_test_results).exec_testcase()

    def logcat_thread(self):
        logcatrecorder.LogcatRecorder(self.logcat_file).startLogcat()

    def collect_thread(self):
        thread1 = multithreadcls.StartTestMultiThread(self.testcase_thread)
        thread2 = multithreadcls.StartTestMultiThread(self.logcat_thread)

        thread1.start()
        thread2.start()

        thread1.join()
        # thread2.join()

if __name__ == '__main__':
    start_obj = StartTest()
    # start_obj.testcase_thread()
    start_obj.collect_thread()
