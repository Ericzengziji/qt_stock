#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file  : qt_stock --> fetch_from_baostock.py
@author: zengziji
@time  : 2022-07-01 16:06
@desc  ： 采用baostock接口获取数据，详见地址：http://baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3
"""
import baostock as bs
import pandas as pd

lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

rs = bs.query_history_k_data_plus("sh.600000",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date='2017-01-01', end_date='2017-01-31',
    frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
    print(data_list[-1])
result = pd.DataFrame(data_list, columns=rs.fields)

# result.to_csv("D:/history_k_data.csv", encoding="gbk", index=False)
print(result)

#### 登出系统 ####
bs.logout()