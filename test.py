import pymysql

db = pymysql.connect(host='101.101.218.133',
                     # port=3306,
                     user='root',
                     passwd='1234',
                     db='SBA_3',
                     charset='utf8')

try:
    cursor = db.cursor()
    sql = "SELECT * FROM price"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row_data in result:
        print(row_data[0],
              row_data[1],
              row_data[2],
              row_data[3])
finally:
    db.close()