# -*- coding: utf-8 -*-

'''
导入txt到数据库中
'''
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
import pymysql
from pymysql.cursors import DictCursor
import config
import json


def mysql_connection():
    host = config.dbhost
    user = config.dbuser
    port = 3306
    password = config.dbpassword
    db = config.dbname
    charset = 'utf8'
    limit_count = 3  # 最低预启动数据库连接数量
    pool = PooledDB(pymysql, limit_count, maxconnections=15, host=host, user=user, port=port, passwd=password, db=db,
                    charset=charset,
                    use_unicode=True, cursorclass=DictCursor)
    return pool

def main():
    tag = 'f5bigip'
    pool = mysql_connection()
    con = pool.connection()
    cursor = con.cursor()
    sql = """INSERT INTO urls(url,tag,mark)
                                             VALUES (%s,%s,%s)"""
    '''
    with open('drupal.json','r') as f:
        lines=f.readlines()
        for line in lines:
            line=line.strip('\n')
            try:
                cursor.execute(sql, (line, tag,0))
                con.commit()
            except:
                con.rollback()
    '''
    
    with open('f5-BIGIP.json', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            jsondata = json.loads(line)
            if 'http' not in jsondata['id']:
                if jsondata['id'][-4:] == ':443':

                    try:
                        cursor.execute(sql, ('https://' + jsondata['id'][:-4], tag, 0))
                        con.commit()
                    except:
                        con.rollback()
                else:
                    if jsondata['id'][-3:] == ':80':
                        try:
                            cursor.execute(sql, ('http://' + jsondata['id'][:-3], tag, 0))
                            con.commit()
                        except:
                            con.rollback()

                    else:
                        try:
                            cursor.execute(sql, ('http://' + jsondata['id'], tag, 0))
                            con.commit()
                        except:
                            con.rollback()

            else:
                try:
                    cursor.execute(sql, (jsondata['id'], tag, 0))
                    con.commit()
                except:
                    con.rollback()

if __name__=='__main__':
    main()
