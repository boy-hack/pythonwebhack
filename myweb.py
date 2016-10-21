#!/usr/bin/env python
# coding=utf-8

from flask import Flask,render_template,request
import re
import baiduip

app = Flask(__name__)


@app.route('/',methods=["get","post"])
def index():
    return render_template('ip.html')

@app.route('/ip',methods=["post"])
def BaiduIp():
    ip = request.form.get("search")
    addr=ip.strip().split('.')  #切割IP地址为一个列表
    if len(addr) != 4:
        return "IP ERROR!"
    data = baiduip.search(ip)
    return render_template('ip.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
