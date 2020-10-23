import pymysql


class Database():
    def __init__(self):
        self.db = pymysql.connect(host='101.101.218.133',
                                  # port=3306,
                                  user='root',
                                  passwd='1234',
                                  db='SBA_3',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        print('row = ', row)
        return row

    def commit(self):
        self.db.commit()
