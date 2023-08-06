#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file  : qt_stock --> ma.py
@author: zengziji
@time  : 2023-08-06 16:10
@desc  ： 
"""
import numpy as np


def get_ma_array(ma_len, value, arr=None):
    """

    :param ma_len:
    :param arr: np.array([])
    :return: np.array([])
    """
    value = float(value)
    arr = np.array([]) if arr is None else arr
    if len(arr) < ma_len:
        arr = np.append(arr, value)
    else:
        arr[:ma_len-1] = arr[1:]
        arr[-1] = value
    return arr


if __name__ == '__main__':
    from a_fetch_data.fetch_data import GetStockData
    import matplotlib.pyplot as plt

    stock_code = '600036'
    stock_df = GetStockData(stock_code).get_history_data_baostock(start_date="2023-01-01", end_date="2023-08-05", frequency="d")
    stock_df.set_index(["date"], inplace=True) # 将日期变成index，这样画图横坐标才能为日期
    stock_df['ma'] = 0.0
    ma_len, arr = 20, None
    for index, row in stock_df.iterrows():
        arr = get_ma_array(ma_len, value=row.close, arr=arr)
        stock_df.loc[index, 'ma'] = arr.mean()

    stock_df[["close", "ma"]].plot(title=stock_code + " price&ma", grid=True)
