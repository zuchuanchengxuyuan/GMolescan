# -*- coding: utf-8 -*-
'''
flask
flask_sqlalchemy
pymysql
python-telegram-bot
'''
import flask
from flask import request,send_from_directory,make_response
from flask_sqlalchemy import SQLAlchemy
import pymysql
import base64
#import telegram
import sys
import os
pymysql.install_as_MySQLdb()
#bot=telegram.Bot(token='1549146362:AAEtzUzrvLof8TIJR2vLYGA_vtWV_XwWwrE')
#bot=telegram.Bot(token='1083384445:AAEWqu1LiIJViw7P-1E-2ttxwJPUvmqGI58')

server=flask.Flask(__name__)
'''
1.查询当前id值
2.更新id值
3.查询当前id值对应的域名压缩传输
'''
class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = '217dcd8cbe468cc1'
    database = 'japanurls'
    server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user,password,database)
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    server.config['SQLALCHEMY_ECHO'] = True
    # 禁止自动提交数据处理
    server.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

# 读取配置
server.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(server)

class exploitscan(db.Model):
    # 定义表名
    __tablename__ = 'exploitscan'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    page = db.Column(db.Integer)
    exploitname= db.Column(db.String(30), unique=True)
    remoteip= db.Column(db.String(30))


class webshellresult(db.Model):
    # 定义表名
    __tablename__ = 'webshellresult'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    url = db.Column(db.String(100))
    exploitname = db.Column(db.String(30))
    resp=db.Column(db.String(100))
    remoteip= db.Column(db.String(30))

class urls(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(100),unique=True)
    tag = db.Column(db.String(30))
    mark=db.Column(db.Integer)

class cvelist(db.Model):
    __tablename__ = 'cvelist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(30))
    exploitname = db.Column(db.String(30))


@server.route("/initplugin",methods=['get'])
def runplugin():
    resultcve = exploitscan.query.filter_by(page=0).all()
    if len(resultcve)>0:
        urltag=cvelist.query.filter_by(exploitname=resultcve[0].exploitname)

        return resultcve[0].exploitname+','+urltag[0].tag
    else:
        resultcve = exploitscan.query.filter(exploitscan.page>0).all()
        if len(resultcve) > 0:
            for i in resultcve:
                urltag=cvelist.query.filter_by(exploitname=i.exploitname)
                exprest=urls.query.filter_by(tag=urltag[0].tag).offset(i.page+1).limit(100).all()
                if len(exprest)==100:
                    return i.exploitname+','+urltag[0].tag

@server.route("/getdata",methods=['get','post'])
def getdata():
    exploitname = request.values.get('exploitname')
    ip = request.remote_addr
    resulttag = cvelist.query.filter_by(exploitname='%s' % exploitname).first()
    print(resulttag)
    result= exploitscan.query.filter_by(exploitname='%s' %exploitname).first()
    print(result)
    num = result.page * 100
    exploitnames=[]
    exprest=urls.query.filter_by(tag=resulttag.tag).offset(num).limit(100)
    for i in exprest:
        exploitnames.append(i.url)
    result.page = result.page + 1
    result.remoteip=ip
    db.session.commit()
    return str(exploitnames)

@server.route("/scanresult",methods=['post'])
def es():
    data=request.form
    pdata = data['resp']
    url,exploitname,resp=str(base64.b64decode(pdata), encoding = "utf-8").split('|')
    remoteip = request.remote_addr
    webshellrole=webshellresult(url=url,exploitname=exploitname,resp=resp,remoteip=remoteip)
    db.session.add(webshellrole)
    db.session.commit()
    return 'good'

@server.route("/search",methods=['get','post'])
def webshellsearch():
    exploitname = request.values.get('exploitname')
    page = request.values.get('page')
    shellresult = []
    num = page* 20
    if exploitname!='':
        exprest = webshellresult.query.filter_by(exploitname=exploitname).offset(num).limit(20)
        print(exprest)
        for i in exprest:
            shellresult.append(i.url)
    else:
        exprest = webshellresult.query.offset(num).limit(20)
        for i in exprest:
            shellresult.append(i.url)
    return str(shellresult)

@server.route('/download',methods=['GET'])
def download():
    filename=request.values.get('file')
    exec_path=os.getcwd()
    file_path='/'.join([exec_path,filename])
    if os.path.exists(file_path):
        return make_response(send_from_directory('./',filename,as_attachment=True))
    else:
        return '{} no file{}'.format(exec_path,filename)

if __name__== '__main__':
    db.create_all()
    server.run(debug=True,port = 9090,host='0.0.0.0')
