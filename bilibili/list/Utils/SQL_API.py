# encoding: utf-8

"""
@version: v1.0
@author: nyansama
@contact: nyansama@163.com
@software: PyCharm
@file: SQL_API.py
@time: 2016/12/22 15:13
"""
import pymysql as sql


# this api is write for with statement
class SQL_API:
    def __init__(self, dbname):
        # print("__init__")
        self._dbname = dbname
        self._conn = sql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db=self._dbname,charset='utf8')
        self.cur = self._conn.cursor()
        pass

    # def __enter__(self):
    #     print("__ENTER__")
    #     self._conn = sql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db=self._dbname)
    #     self.cur = self._conn.cursor()
    #     return self

    def init_db(self):
        self.init_types()
        pass

    def init_anime(self):
        sql_str = "CREATE TABLE anime(id INTEGER PRIMARY KEY NOT NULL, \
                   name VARCHAR(150) NOT NULL , \
                   cover VARCHAR ,\
                   favorite INT ,\
                   pub_time INT ,\
                   status INT ,\
                   total_count INT ,\
                   update_time INT ,\
                   url VARCHAR ,\
                   week INT ,\
                   country INT ,\
                   types INT );"
        self.cur.execute(sql_str)
        pass

    def init_cast(self):
        sql_str = "CREATE TABLE cast(id INT PRIMARY KEY NOT NULL ,\
                   name VARCHAR(50) NOT NULL, \
                   );"
        self.cur.execute(sql_str)
        pass

    def init_ccr(self):
        sql_str = "CREATE TABLE anime_cast(id INT PRIMARY KEY NOT NULL ,\
                   anime_id INT NOT NULL, \
                   cast_id INT NOT NULL);"
        self.cur.execute(sql_str)
        pass

    def init_types(self):
        sql_str = "CREATE TABLE types(id INT PRIMARY KEY NOT NULL ,\
                   name VARCHAR(50) NOT NULL \
                   );"
        self.cur.execute(sql_str)
        pass


    def clear_table(self,tbname):
        sql_str = "DROP TABLE %s ;" % tbname

        self.cur.execute(sql_str)

    # def test_api(self):
    #     print("Hello World!")

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     print("__EXIT__")
    #     self.cur.close()
    #     self._conn.commit()
    #     self._conn.close()

    def __del__(self):
        # print("__DEL__")
        self.cur.close()
        self._conn.commit()
        self._conn.close()
        pass


if __name__ == '__main__':
    pass
