# -*- coding:utf-8 -*-
from config.settings import db

# 简单获取数据
def get(table, **kw):
    return db.select(table, **kw)

# 对于一个复杂查询，可以直接使用sql语句
def getbysql(sql, vars=None, processed=False, _test=False):
    return db.query(sql, vars, processed, _test)

# 简单插入数据
def add(table, **kw):
    return db.insert(table, **kw)

# 简单获取数据的数量
def getcount(table, column='*', where='', group=''):
    sql = 'select count(' + column + ') as total_count from ' + table
    if where != '':
        sql += ' where ' + where
    if group != '':
        sql += ' group by ' + group
    results = db.query(sql)
    return results[0].total_count

# 简单更新
def update(table, **kw):
    return db.update(table, **kw)

# 简单删除
def delete(table, **kw):
    return db.delete(table, **kw)
