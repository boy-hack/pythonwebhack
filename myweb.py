#!/usr/bin/env python
# coding=utf-8

from flask import Flask,render_template,request
import re
import baiduip
import cms
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/',methods=["get","post"])
def index():
    return render_template('ip.html')

#IP地址定位
@app.route('/ip',methods=["get","post"])
def BaiduIp():
    if request.method == 'POST':
        ip = request.form.get("search")
        addr=ip.strip().split('.')  #切割IP地址为一个列表
        if len(addr) != 4:
            return "IP ERROR!"
        data = baiduip.search(ip)
        return render_template('ip.html',data=data,title="高精度IP查询")
    else:
        return render_template('ip.html',title="高精度IP查询")

#CMS在线识别
@app.route('/webdna',methods=["get","post"])
def webdna():
    if request.method == 'POST':
        url = request.form.get("search")
        if re.match(r'^https?:/{2}\w.+$', url):
            data = cms.cms(url)
            if data is False:
                data["error"] = "没有找到合适的CMS"
        return render_template('cms.html',data=data,title="CMS识别")
    else:
        return render_template('cms.html',title="CMS识别")

if __name__ == '__main__':
    app.run(debug=True)
