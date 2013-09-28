#!/usr/bin/python
#coding=utf-8
import sqlite3
import MySQLdb

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class sqliteDB(object):
    """docstring for sqliteDB"""
    def __init__(self, dbFile='MyData.sqlite3'):
        self.conn = sqlite3.connect('MyData.sqlite3')
        self.conn.row_factory = dict_factory

    def fetchall(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception:
            return None
        finally:
            cursor.close()

    def insert(self, table, data):
        keys   = ""
        values = ""
        try:
            for key in data.keys():
                keys += key + ","
                values += "\"" + str(data[key]) + "\","
        except Exception, e:
            print e

        keys = keys[:-1]
        values = values[:-1]
        sql = "insert into " + table + " (" + keys + ") "+" values "+" ("+values+");"
        print sql
        self.conn.execute(sql)
        self.conn.commit()

    def update(self, table, data, condition):
        sqlArray = []
        for key in data.keys():
            sqlArray.append('%s ="%s"' % (key, data[key]))

        sql = "update "+table+" set "+','.join(sqlArray)+" where "+condition + ';'
        self.conn.execute(sql)
        self.conn.commit()

    def delete(self, table, condition):
        sql = "delete from " + table + " where " + condition + ';'
        self.conn.execute(sql)
        self.conn.commit()


    def close(self):
        self.conn.close()


if __name__ == '__main__':
    dbUtil = sqliteDB()
    dbUtil.delete('Selection', 'TestType in (1004, 1005, 1006)')

    print dbUtil.fetchall('select * from Selection where TestType=1004')