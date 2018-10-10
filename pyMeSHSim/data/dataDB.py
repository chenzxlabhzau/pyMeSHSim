# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3

import pymysql

class dataDB(object):
    def __init__(self):
        self.host = "localhost"
        self.userName = "zhluo"
        self.password = "luozh123"
        self.database = "umls"
        self.db = pymysql.connect(self.host, self.userName, self.password, self.database)
        self.cursor = self.db.cursor()

    def fetch_all(self, sql_cmd=None):
        self.cursor.execute(sql_cmd)
        result = self.cursor.fetchall()
        return result

    def fetch_one(self, sql_cmd=None):
        self.cursor.execute(sql_cmd)
        result = self.cursor.fetchone()
        return result



if __name__ == '__main__':
    dataclient = dataDB()