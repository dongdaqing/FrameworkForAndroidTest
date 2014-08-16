# -*- coding: utf8 -*-
'''
@author: qing
'''
import utils.loggingmodule
import os
import platform
class DeviceInfo(object):
    def __init__(self):
        pass

    def parseDeviceInfo(self):

        brand = ''
        model = ''
        version = ''
        density = ''
        sys_info = platform.system()
        if sys_info == "Windows":
            adbDensityInfo = os.popen('adb shell getprop | find "density"').read()
        elif sys_info == "Linux":
            adbDensityInfo = os.popen('adb shell getprop | grep "density"').read()
        else:
            adbDensityInfo = os.popen('adb shell getprop | grep "density"').read()
        densityInfo_detail = adbDensityInfo.split(' ')
        for density_info in range(len(densityInfo_detail)-1,-1,-1):
            if densityInfo_detail[density_info].find('[') != -1:
                    index_d = densityInfo_detail[density_info].find(']')
                    density = densityInfo_detail[density_info].strip()[1:index_d]
                    break
        adbDeviceInfo = os.popen('adb shell cat /system/build.prop').read()
        deviceInfo = adbDeviceInfo.split('\n')
        for i in range(0,len(deviceInfo)):
            device_info_detail = deviceInfo[i]
            if device_info_detail.find('brand') != -1:
                    index_b = device_info_detail.find('=')
                    brand = device_info_detail.strip()[index_b+1:]
                        
            if device_info_detail.find('model') != -1:
                    index_m = device_info_detail.find('=')
                    model = device_info_detail.strip()[index_m+1:]

            if device_info_detail.find('build.version.release') != -1:
                    index_v = device_info_detail.find('=')
                    version = device_info_detail.strip()[index_v+1:]
                        
        return (brand,model,version,density)
if __name__=='__main__':
    info=DeviceInfo().parseDeviceInfo()
    