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
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from mplfinance.original_flavor import candlestick_ochl
    from matplotlib.dates import date2num
    from datetime import datetime
    plt.rcParams['font.sans-serif'] = ['SimHei']

    stock_code = '600036'
    stock_df = GetStockData(stock_code).get_history_data_baostock(start_date="2023-03-01", end_date="2023-08-05",
                                                                  frequency="d")
    stock_df.set_index(["date"], inplace=True)
    stock_df['ma'], stock_df['buy'], stock_df['sell'], stock_df['hold_money'] = 0.0, None, None, 0.0
    ma_array, left_money, hold_vol = None, 100000, 0
    for index, row in stock_df.iterrows():
        order_siganl_bool, ma_array, left_money, per_vol,hold_vol = ma_stragety(current_price=row['close'], threshold=0.05, hist_array=ma_array, left_money=left_money, hold_vol=hold_vol)
        stock_df.loc[index, 'ma'] = ma_array.mean()
        stock_df.loc[index, 'hold_money'] = left_money + hold_vol * float(row['close'])

        if order_siganl_bool["buy"]:
            stock_df.loc[index, 'buy'] = row['close']
        elif order_siganl_bool["sell"]:
            stock_df.loc[index, 'sell'] = row['close']

    figure, axes = plt.subplots(nrows=3, ncols=1)
    axes[0].xaxis.set_major_locator(ticker.MultipleLocator(100))
    axes[0].plot(stock_df.index, stock_df.close, c='black', label='price') # 颜色只有 black white red yellow green cyan青色 blue magent紫色
    axes[0].plot(stock_df.index, stock_df.ma, c='blue', label='ma')
    axes[0].scatter(stock_df.index, stock_df.buy, c='red', label='buy', marker='o', alpha=0.5)
    axes[0].scatter(stock_df.index, stock_df.sell, c='green', label='sell', marker='o', alpha=0.5)
    axes[0].legend(loc=0)
    axes[0].set_title(stock_code)
    axes[0].grid()

    axes[1].plot(stock_df.index, stock_df.hold_money - 100000, c='red', label='ma')
    axes[1].xaxis.set_major_locator(ticker.MultipleLocator(100))
    axes[1].set_title('profit')

    stock_df['datetime'] = stock_df.index
    stock_df['datetime'] = stock_df['datetime'].apply(lambda x:date2num(datetime.strptime(x, "%Y-%m-%d")))

    candlestick_ochl(
        axes[2],
        stock_df.loc[:, ['datetime', 'open', 'close', 'high', 'low']].values,
        width=0.2,
        colorup='r',
        colordown='g',
        alpha=1.0
    )
    axes[2].set_xticklabels(stock_df['datetime'].to_list())
    axes[2].set_title('K线图')





