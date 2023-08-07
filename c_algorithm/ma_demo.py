#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file  : qt_stock --> ma_demo.py
@author: zengziji
@time  : 2023-08-06 16:22
@desc  ： 输入一行股票信息返回时否出现买入或者卖出信号，注意内存大小的控制
"""
from b_process_data import ma


def ma_stragety(current_price, ma_len = 20, threshold=0.02, hist_array=None, left_money=100000, per_vol=300, hold_vol=0):
    """

    :param current_price:
    :param ma_len: ma的长度
    :param threshold: 触发信号的阈值比例，1+-threshold 范围为0~1
    :return: 返回买卖信号
    """
    ma_array = ma.get_ma_array(ma_len=ma_len, arr=hist_array, value=current_price)
    order_siganl_bool = {"buy":False, "sell":False}

    if ma_len == len(ma_array):
        if current_price < ma_array.mean() * (1-threshold) and left_money-per_vol*current_price > 0:
            order_siganl_bool["buy"] = True
            hold_vol += per_vol
            left_money -= per_vol * current_price

        elif current_price > ma_array.mean() * (1+threshold) and hold_vol >= per_vol:
            order_siganl_bool["sell"] = True
            hold_vol -= per_vol
            left_money += per_vol * current_price

    return order_siganl_bool, ma_array, left_money, per_vol, hold_vol


if __name__ == '__main__':
    from a_fetch_data.fetch_data import GetStockData
    from f_common_tools.plot_utils import plot_picture
    stock_code = '600036'
    result_df = GetStockData(stock_code).get_history_data_baostock(start_date="2023-03-01", end_date="2023-08-05",
                                                                  frequency="d")
    result_df.set_index(["date"], inplace=True)
    result_df['ma'], result_df['buy'], result_df['sell'], result_df['hold_money'] = 0.0, None, None, 0.0
    ma_array, left_money, hold_vol = None, 100000, 0
    for index, row in result_df.iterrows():
        order_siganl_bool, ma_array, left_money, per_vol,hold_vol = ma_stragety(current_price=row['close'], threshold=0.05, hist_array=ma_array, left_money=left_money, hold_vol=hold_vol)
        result_df.loc[index, 'ma'] = ma_array.mean()
        result_df.loc[index, 'hold_money'] = left_money + hold_vol * float(row['close'])

        if order_siganl_bool["buy"]:
            result_df.loc[index, 'buy'] = row['close']
        elif order_siganl_bool["sell"]:
            result_df.loc[index, 'sell'] = row['close']

    # 计算利润
    result_df['profit'] = result_df['hold_money'] - 100000

    # style = [{'line':['close', 'ma'], 'scatter':['buy', 'sell'], 'title':None}, {'line':['profit'], 'title':'profit'}, {'candel':['k'], 'title':'K'}]
    style = [{'line': ['close'], 'scatter': ['buy', 'sell'], 'title': None},
             {'line': ['profit'], 'title': 'profit'}, {'candel':['k'], 'title':'K'}]
    # axes = plot_picture(result_df, style=style, x_show_nums=5)
    axes = plot_picture(result_df, x_show_nums=5)


