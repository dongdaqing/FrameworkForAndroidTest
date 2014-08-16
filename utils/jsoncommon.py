# -*- coding: utf-8 -*-
__author__ = 'dongdaqing'
import os,codecs,json
false = False
class ParseJson(object):

    def __init__(self):
        self.value=[]
        self.key_dic=[]

    def print_keyvalue_all(self,input_json):
        key_value=''
        if isinstance(input_json,dict):
            for key in input_json.keys():
                key_value = input_json.get(key)
                if isinstance(key_value,dict):
                    self.print_keyvalue_all(key_value)
                elif isinstance(key_value,list):
                    for json_array in key_value:
                        self.print_keyvalue_all(json_array)
                else:
                    print str(key)+" = "+str(key_value)
        elif isinstance(input_json,list):
            for input_json_array in input_json:
                self.print_keyvalue_all(input_json_array)

    def print_keyvalue_by_key(self,input_json,key):
        key_value=''
        if isinstance(input_json,dict):
            for json_result in input_json.values():
                if key in input_json.keys():
                    key_value = input_json.get(key)
                    self.value = key_value
                else:
                    self.print_keyvalue_by_key(json_result,key)
        elif isinstance(input_json,list):
            for json_array in input_json:
                self.print_keyvalue_by_key(json_array,key)
        if key_value!='':
#            print str(key)+" = "+str(key_value)
            pass
 #           print self.value
        return self.value
    #按jsonarray中的key及keyvalue检索（因为body中key很多，需要找特定的keyvalue）返回
    #例如查找key=n3且keyvalue=“搜索结果页”，返回值为该body中的e字段
    def get_keyvaluedic_by_key(self,input_json,key,key_value,returnvalue):
        
        if isinstance(input_json,dict):
            for json_result in input_json.values():
                if key in input_json.keys():
                    keyvalue = input_json.get(key)
#                    print key_value,keyvalue
                    if str(keyvalue) == key_value:
                         self.value = str(key_value)
                         self.key_dic=input_json.get(returnvalue)
#                         print self.key_dic
                         
                else:
                    self.get_keyvaluedic_by_key(json_result,key,key_value,returnvalue)
        elif isinstance(input_json,list):
            for json_array in input_json:
                self.get_keyvaluedic_by_key(json_array,key,key_value,returnvalue)
#        if key_value!='':
#            print str(key)+" = "+str(key_value)
#           print self.value
        return self.key_dic
    #查询key:keyvalue所在json小组的所有参数
    def get_keyvalueset(self,input_json,key,keyvalue):
        key_value=''
        if isinstance(input_json,dict):
            for json_result in input_json.values():
                if key in input_json.keys():
                    if keyvalue == input_json.get(key):
                        self.value = input_json.keys()
                else:
                    self.get_keyvalueset(json_result,key,keyvalue)
        elif isinstance(input_json,list):
            for json_array in input_json:
                self.get_keyvalueset(json_array,key,keyvalue)

        return self.value
    
if __name__=='__main__':
    filename=r'd:\sdklog.log'
    f = codecs.open(filename,'r','utf-8')
    lines = f.readlines()

#            print lines[index]
    if lines[len(lines)-2].find("2014")!=-1:
        pos=lines[len(lines)-2].find("{")
        json_line=lines[len(lines)-2][pos:]
        print json_line                  
        dict_line = eval(json_line)
                #第1列写入Note              
        note=ParseJson().get_keyvaluedic_by_key(dict_line, "n3","请求视频信息",'e')
        print note