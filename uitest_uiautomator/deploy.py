__author__ = 'dongdaqing'

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/utils/")
import loggingmodule

class Deploy(object):
    
    def __init__(self,uiautomator_test_results):
        self.logger = loggingmodule.Logger('uiautomator_test', uiautomator_test_results)

        self.project_path = "/Users/dongdaqing/SVN/YoukuMobileTest/AutomatedTesting/Android/UIAutomator/YoukuUIAutomatorTest"
        self.single_test_suite_name = "com.youku.phone.adv.AdvSkippingTest"
        self.play_videos_test = "com.youku.phone.player.PlayVideosTest"

    def prepare_test(self):
        os.chdir(self.project_path)
        return_info = os.popen("ant build").read()
        self.logger.log(return_info)
        return_info = os.popen("adb push {0}/bin/YoukuMobileTest.jar /data/local/tmp".format(self.project_path)).read()
        self.logger.log(return_info)

    def run_single_test_suite(self):
        self.prepare_test()
        # os.system("adb shell uiautomator runtest YoukuMobileTest.jar -c {0}".format(self.single_test_suite_name))
        return_info = os.popen("adb shell uiautomator runtest YoukuMobileTest.jar -c {0}".format(self.play_videos_test)).read()
        self.logger.log(return_info)

    def exec_testcase(self):
        self.run_single_test_suite()
        
if __name__ == '__main__':

    test_file = "/Users/dongdaqing/workspace/Android/temp/test.txt"
    obj_deploy = Deploy(test_file)
    obj_deploy.exec_testcase()
