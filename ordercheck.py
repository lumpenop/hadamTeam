#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def ordcheck():

    import pandas as pd
    import pymysql 
    con = pymysql.connect(host='101.101.218.133',port = 3306,user='root', password='1234', db='SBA_3', charset='utf8')
    cursor = con.cursor()
    sql = "select * from new_table"
    cursor.execute(sql)
    result = cursor.fetchall()


    result = pd.DataFrame(result)
    con.close()
    
    return result

