# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'

import urllib2,json
import os
from xlrd import open_workbook

class PlayControl(object):

    def __init__(self):
        # self.phone_header = {"User-Agent":"Youku;4.2;Android;4.4.2;SM-G9006V","Connection":"Keep-Alive","Accept-Encoding":"gzip"}
        self.phone_header = {"User-Agent":"Youku;4.2;Android;4.4.2;SM-G9006V"}
        self.hd_header = {"User-Agent":"Youku HD;4.2;Android;4.4.2;SM-G9006V"}

    def request_mobile_url(self, header,url):
        request = urllib2.Request(url, headers=header)
        open_url_result = urllib2.urlopen(request)
        request_result = open_url_result.read()
        # try:
        json_result = json.loads(request_result)
        # except Exception:
        #     return "success"
        open_url_result.close()
        return json_result

    def request_web_url(self, url):
        request = urllib2.Request(url)
        open_url_result = urllib2.urlopen(request)
        request_result = open_url_result.read()
        json_result = json.loads(request_result)
        open_url_result.close()
        return json_result

    def get_mobile_response_code(self,header,url):

        json_result = self.request_mobile_url(header,url)
        # if json_result == "success":
        #     return "success"

        if json_result.has_key('code'):
            return json_result['code']
        # elif json_result.has_key('status'):
        #     return json_result['status']
        # elif json_result.has_key["\"blank_num\""]:
        #     return "success"
        else:
            return "success"

    def get_web_response_code(self,url):
        json_result = self.request_web_url(url)
        return json_result['dataset']['permission'][0]['access']

    def get_url_from_excel(self,excel_file):
        wb = open_workbook(excel_file)
        for sheet_index in range(1,4,2):
            sheet_num = wb.sheet_by_index(sheet_index)
            if sheet_index == 1:
                header = self.phone_header
                print "Android Phone:"
                # continue
            else:
                header = self.hd_header
                print "Android Pad:"
            rows = sheet_num.nrows
            for i in range(1,rows):
                row_data = sheet_num.row_values(i)
                case_id = row_data[0]
                video_id = row_data[1]
                mobile_url = row_data[13]
                # web_url = row_data[14]

                if mobile_url != '':
                    mobile_response = self.get_mobile_response_code(header,mobile_url)
                    print int(case_id), int(video_id), 'mobile_api_response_result: '+str(mobile_response)

    def start_test(self):
        root_path = os.path.dirname(__file__)
        test_excel = os.path.join(root_path,"线上部分播控数据北京.xls")
        play_control_obj = PlayControl()
        play_control_obj.get_url_from_excel(test_excel)

if __name__ == '__main__':
    play_control_obj = PlayControl()
    play_control_obj.start_test()