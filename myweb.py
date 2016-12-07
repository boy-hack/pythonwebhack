#!/usr/bin/env python
# coding=utf-8

from flask import Flask,render_template,request
import re
import baiduip
from password import PasswdGenerator
import cms
import sys
import whois
import skg

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



app = Flask(__name__)
#连接数据库操作
db = MySQLdb.connect("127.0.0.1","root","","pyhack",charset='utf8' )
cursor = db.cursor()

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

#在线密码生成
@app.route('/password',methods=["get","post"])
def password_build():
    if request.method == 'POST':
        from flask import make_response
        birthday = request.form.get("birthday","")
        fullname = request.form.get("fullname","")
        nickname = request.form.get("nickname","")
        englishname = request.form.get("englishname","")
        partnername = request.form.get("partnername","")
        phone = request.form.get("phone","")
        qq = request.form.get("qq","")
        company = request.form.get("company","")
        domain = request.form.get("domain","")
        oldpasswd = request.form.get("oldpasswd","")
        keywords = request.form.get("keywords","")
        keynumbers = request.form.get("keynumbers","")
        pwgen = PasswdGenerator(fullname=fullname,nickname=nickname,englishname=englishname,partnername=partnername,phone=phone,qq=qq,company=company,domain=domain,oldpasswd=oldpasswd,keywords=keywords,keynumbers=keynumbers,birthday=birthday)
        wordlist = pwgen.generate()
        content = '\n'.join(wordlist)
        #content = "long text"
        response = make_response(content)
        response.headers["Content-Disposition"] = "attachment; filename=pass.txt"
        return response
        #return render_template('password.html',data=wordlist,title="社工密码生成")
    else:
        return render_template('password.html',title="社工密码生成")

#Whois 在线查询
@app.route('/whois',methods=["get","post"])
def whoisa():
    if request.method == 'POST':
        url = request.form.get("search")
        data = whois.whois(url).replace("\n","</br>")
        return render_template('whois.html',data=data,title="Whois查询")
    else:
        return render_template('whois.html',title="Whois查询")

#调用外部社工库进行查询
@app.route('/pass',methods=["get","post"])
def findpass():
    if request.method == 'POST':
        info = request.form.get("search")
        data = skg.findpass(info)
        return render_template('skg.html',data=data,title="社工库查询")
    else:
        return render_template('skg.html',title="社工库查询")

#集成wooyun漏洞平台
@app.route('/wooyun',methods=["get","post"])
@app.route('/wooyun/<int:pages>',methods=["get","post"])
def wooyun(pages = 0):
    searchword = request.args.get('key', '').strip()
    log_id = request.args.get('id', '').strip()
    data = {}
    table = list()
    if log_id:
        # 使用execute方法执行SQL语句
        cursor.execute(MySQLdb.escape_string("SELECT * from emlog_blog where gid=%s"%log_id))
        # 使用 fetchone() 方法获取一条数据库。
        results = cursor.fetchone()
        data["id"] = results[0]
        data["text"] = results[2]
        data["title"] = results[1]
    if searchword:
        sql = 'SELECT gid,title from emlog_blog where title like "%%%s%%"'%(searchword)
        cursor.execute(sql)
        #cursor.execute('SELECT * from emlog_blog limit 10')
        results = cursor.fetchall()

        for rows in results:
            tdata = {}
            tdata["id"] = rows[0]
            tdata["title"] = rows[1]
            table.append(tdata)
    return render_template("wooyun.html",title="乌云漏洞查询",data=data,table=table)

#集成wooyun漏洞平台 -被忽略的漏洞
@app.route('/wooyun1',methods=["get","post"])
@app.route('/wooyun1/<int:pages>',methods=["get","post"])
def wooyun1(pages=0):
    if pages is None:
        pages = 0
    if pages < 0:
        pages = 0
    sql = 'SELECT gid,title from emlog_blog where content like "%%%s%%" limit %d,%d'%("无影响厂商忽略",pages*20,20)
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    table = list()
    for rows in results:
        tdata = {}
        tdata["id"] = rows[0]
        tdata["title"] = rows[1]
        table.append(tdata)
    return render_template("wooyun.html",title="乌云忽略漏洞查询",table=table,next=pages+1,prev=pages-1)

if __name__ == '__main__':
    app.run(debug=True)
