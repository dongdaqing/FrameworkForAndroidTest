# -*- coding: utf-8 -*-

import os,sys,re
import subprocess,codecs,time,platform
import utils.loggingmodule

class GenAPK(object):

    def __init__(self,filename):

        sys_info = platform.system()
        if sys_info == "Windows":
            common_devsvn_path = r"D:\svn"
            other_path = r"D:\svn\repos\AutomatedTesting\DailyBuild\uitest"
        elif sys_info == "Linux":
            common_devsvn_path = ""
            other_path = ""
        else:
            common_devsvn_path = r"/Users/dongdaqing/SVN/AndroidDev"
            other_path = r"/Users/dongdaqing/SVN/MobileTest/DongDaqing/DailyBuild/PyProject/uitest"

        u"""Define config dir"""
        self.trackerpath = os.path.join(common_devsvn_path,r"androidpublic/tags/YKanTracker_3.1_Release")
        self.absPath = os.path.join(common_devsvn_path,r"android_youku/tags/abs_3.1_Release")
        self.phonePath = os.path.join(common_devsvn_path,r"android_youku/tags/Youku_Mobile_3.1.2_Release")
        self.binYouku_Mobile = os.path.join(common_devsvn_path,r"android_youku/tags/Youku_Mobile_3.1.2_Release/bin")
        self.binYKanTracker = os.path.join(common_devsvn_path,r"androidpublic/tags/YKanTracker_3.1_Release/bin")
        self.binAbs = os.path.join(common_devsvn_path,r"android_youku/tags/abs_3.1_Release/bin")
        self.pgkDir = other_path
        self.keyStoreFile = os.path.join(other_path,"debug.keystore")

        if sys_info == "Windows":
            self.trackerpath=self.trackerpath.replace("/",os.sep)
            self.absPath=self.absPath.replace("/",os.sep)
            self.phonePath=self.phonePath.replace("/",os.sep)
            self.binYouku_Mobile=self.binYouku_Mobile.replace("/",os.sep)
            self.binYKanTracker=self.binYKanTracker.replace("/",os.sep)
            self.binAbs=self.binAbs.replace("/",os.sep)
            self.pgkDir=self.pgkDir.replace("/",os.sep)
            self.keyStoreFile=self.keyStoreFile.replace("/",os.sep)
        elif sys_info == "Linux":
            common_devsvn_path = ""
            other_path = ""
        else:
            self.trackerpath=self.trackerpath.replace("\\",os.sep)
            self.absPath=self.absPath.replace("\\",os.sep)
            self.phonePath=self.phonePath.replace("\\",os.sep)
            self.binYouku_Mobile=self.binYouku_Mobile.replace("\\",os.sep)
            self.binYKanTracker=self.binYKanTracker.replace("\\",os.sep)
            self.binAbs=self.binAbs.replace("\\",os.sep)
            self.pgkDir=self.pgkDir.replace("\\",os.sep)
            self.keyStoreFile=self.keyStoreFile.replace("\\",os.sep)
        u"""initial logger"""
        self.log1 = utils.loggingmodule.Logger('genapk',filename)

    def updateCode(self):
        self.log1.log('更新abs工程目录')
        os.chdir(self.absPath)
        self.exec_cmd('svn update .')
        self.log1.log('更新youkutracker工程目录')
        os.chdir(self.trackerpath)
        self.exec_cmd('svn update .')
        self.log1.log('更新youkumobile工程目录')
        os.chdir(self.phonePath)
        self.exec_cmd('svn update .')

    def exec_cmd(self,cmd):
        return subprocess.call(cmd, shell=True)

    def initialBinDir(self):
        if not os.path.exists(self.binYouku_Mobile):
            os.mkdir(self.binYouku_Mobile)
        if not os.path.exists(self.binYKanTracker):
            os.mkdir(self.binYKanTracker)
        if not os.path.exists(self.binAbs):
            os.mkdir(self.binAbs)

    def exec_pkg(self):
        u"""开始打包"""
        os.chdir(self.binYouku_Mobile)

        os.chdir(self.absPath)
        self.exec_cmd('ant clean')
        self.exec_cmd('android update project -p .')
        os.chdir(self.trackerpath)
        self.exec_cmd('ant clean')
        self.exec_cmd('android update project -p .')
        os.chdir(self.phonePath)
        self.exec_cmd('ant clean')
        self.exec_cmd('android update project -p .')
        self.exec_cmd('ant release')

        os.chdir(self.binYouku_Mobile)
        antReleaseSigner = 'jarsigner -verbose -keystore {0} -storepass android -signedjar Youku_Android_ForTest.apk \
    ActivityWelcome-release-unsigned.apk androiddebugkey'.format(self.keyStoreFile)
        print antReleaseSigner
        self.exec_cmd(antReleaseSigner)

        self.exec_cmd('copy Youku_Android_ForTest.apk {0}'.format(self.pgkDir))

    def genApk(self):
        start = time.time()
        #删除目录中的历史安装包
        self.exec_cmd('rm Youku_Android_ForTest.apk')
        self.initialBinDir()
        self.updateCode()
        self.log1.log('开始打包－－－－－－－－－')
        self.exec_pkg()
        self.log1.log('打包结束－－－－－－－－－')
        end = time.time()
        print 'APK Complie Finish!'
        print 'Using time(s):',end-start

if __name__ == '__main__':
    apkObj=GenAPK()
    apkObj.genApk()
