#!/usr/bin/env python
# coding=utf-8

"""
社工库调用
"""

import requests
import json

def findpass(username):
    payload = {'q':username}
    headers = {"Accept":"application/json, text/javascript, */*; q=0.01",
               "User-Agent":"Mozilla/5.0 (Windows NT 9.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
               "Referer":"http://www.fangzhuangku.com/pwd"}
    r = requests.post("http://www.fangzhuangku.com/function/pwdsearch.php",data = payload,headers=headers)
    s = json.loads(r.text)
    sdata = s["data"]
    dict = list()
    if len(sdata):
        for key in sdata:
            for key1 in sdata[key]:
                ls_data = {'u':'','p':'','e':'','s':key}
                if 'u' in key1.keys():
                    ls_data["u"] = key1["u"]
                if 'p' in key1.keys():
                    ls_data["p"] = key1["p"]
                if 'e' in key1.keys():
                    ls_data["e"] = key1["e"]
                dict.append(ls_data)
    return dict
if __name__ == '__main__':
    pass