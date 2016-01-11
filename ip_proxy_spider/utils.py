#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2014-7-23

@author: chen
'''
import datetime
import mysql.connector
import settings
import traceback

def get_time_now():
    return '\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " [CUSTOM INFO]"
    
def disable_ip(ip, port):
    conn = mysql.connector.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, password=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME)
    cursor = conn.cursor()
    sqlStr = "update ip_proxy_info i set i.isvalid=0 where i.ip='%s' and i.port='%s'" % (ip, port)
    
    try:
        cursor.execute(sqlStr)    
        print get_time_now(), 'Disableing ip proxy %s' % ip
    except:
        print get_time_now(), traceback.print_exc()
        
    conn.commit()
    cursor.close()
    conn.close()
                        
