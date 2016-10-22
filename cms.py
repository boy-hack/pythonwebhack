#!/usr/bin/env python
# coding=utf-8

"""
Function: CMS识别系统
Author:   w8ay
Time:     2016年10月21日 16/17/33
"""

import requests
import hashlib
import socket
import os

data = []
socket.setdefaulttimeout(10)

def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def getmd5(url):
    src = requests.get(url).content
    md5=get_md5_value(src)
    return md5

def init():
    file_url = os.path.abspath(os.path.split(os.path.realpath(__file__))[0] + r"./config/dna.txt")
    file = open(file_url)
    try:
        for line in file:
            str = line.strip().split(" ")
            ls_data={}
            if len(str)==3:
                ls_data["url"] = str[0]
                ls_data["name"] = str[1]
                ls_data["md5"] = str[2]
                data.append(ls_data)
    finally:
        file.close( )

def cms(url):
    if url is None:
        print "url is Null!"
        return
    url = url.rstrip("/")
    for dataline in data:
        _url = url + dataline["url"]
        #print "Scan " + _url
        try:
            status = requests.head(_url,timeout=10).status_code
        except:
            pass

        if status==200:
            md5 = get_md5_value(requests.get(_url).content)
            #print md5
            if(md5 == dataline["md5"]):
                dataline["url"] = _url
                return dataline
    return False

#初始化载入字典
init()
if __name__ == '__main__':
    pass