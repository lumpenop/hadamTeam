#!/usr/bin/env python
# coding: utf-8

# In[ ]:



def ordcancel():
    import pandas as pd
    import pymysql 
    
    dnum = input("취소할 주문 번호 입력\n")

    con = pymysql.connect(host='101.101.218.133',port = 3306,user='root', password='1234', db='SBA_3', charset='utf8')
    cursor = con.cursor()
    sql2 = "delete from new_table where order_num={}".format(dnum)
    cursor.execute(sql2)
    con.commit()


    sql = "select * from new_table"
    cursor.execute(sql)
    result = cursor.fetchall()


    result = pd.DataFrame(result)
    con.close()

    print("{}번 주문이 취소되었습니다.".format(dnum))
    
    return(result)

