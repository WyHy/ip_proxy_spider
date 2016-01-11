# -*- coding: utf-8 -*-

import mysql.connector
import traceback
import utils

def back_up_opt():
    print utils.get_time_now(), 'Working on table back_up job...'
    try:
        conn = mysql.connector.connect(host="10.122.202.19",user="root",password="1qazxsw2",db='ip_proxy_db')
        cursor = conn.cursor()
        
        sqlStr = 'select * from ip_proxy_info;'
        cursor.execute(sqlStr)

        cam_rows = cursor.fetchall()
        if cam_rows:
            cursor.execute('truncate table ip_proxy_info_bak')
            cursor.execute("insert into ip_proxy_info_bak select * from ip_proxy_info where isvalid='1'")
            cursor.execute('truncate table ip_proxy_info')
        
        conn.commit()
        cursor.close()
        conn.close()
    except:
        traceback.print_exc()
    
    print utils.get_time_now(), 'Job is Done.'
    
    
if __name__ == '__main__':
    back_up_opt()