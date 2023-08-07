#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file  : qt_stock --> plot_utils.py
@author: zengziji
@time  : 2023-08-08 0:00
@desc  ： 画图工具
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick_ochl
from matplotlib.dates import date2num
from datetime import datetime
plt.rcParams['font.sans-serif'] = ['SimHei'] # 兼容中文的设置


def plot_picture(result_df, style=[{'line':['close'], 'scatter':['buy', 'sell'], 'title':None}, {'line':['profit'], 'title':'profit'}], **kwargs):
    """

    :param result_df: df基础数据，默认index为日期yyyy-MM-dd格式，默认包含code、close、buy、sell、profit字段
    :param style: 画布样式列表，列表每个元素为dict代表每个画布的配置。 line代表折线 默认显示收盘价格，scatter代表散点，默认显示买卖信号点
    :return:
    """
    nrows = len(style)
    figure, axes = plt.subplots(nrows=nrows, ncols=1)

    # 第一个画布内容
    for index, axe in enumerate(axes):
        x_show_nums = kwargs.get('x_show_nums') if kwargs.get('x_show_nums') is not None else 10
        ticker_space = int(len(result_df)/x_show_nums)
        axe.xaxis.set_major_locator(ticker.MultipleLocator(ticker_space))

        if "line" in style[index].keys():
            for col in style[index]['line']:
                # axes[0].plot(result_df.index, result_df.ma, c='blue', label='ma') # 颜色只有 black white red yellow green cyan青色 blue magent紫色
                axe.plot(result_df.index, result_df[col], label=col)

        if "scatter" in style[index].keys():
            for col in style[index]['scatter']:
                axe.scatter(result_df.index, result_df[col], label=col, marker='o', alpha=1)

        if "candel" in style[index].keys():
            result_df['datetime'] = result_df.index
            result_df['datetime'] = result_df['datetime'].apply(lambda x: date2num(datetime.strptime(x, "%Y-%m-%d")))
            candlestick_ochl(
                axe,
                result_df.loc[:, ['datetime', 'open', 'close', 'high', 'low']].values,
                width=0.2,
                colorup='r',
                colordown='g',
                alpha=1.0
            )
            # axe.set_xticklabels(result_df['datetime'].to_list())
            axe.get_xaxis().set_visible(False) # 不显示横坐标

        title = style[index]['title'] if style[index]['title'] is not None else result_df.code[0]
        axe.set_title(title)
        axe.legend(loc=0) # 设置标签限显示的位置 0 好像是左上角的意思
        axe.grid(alpha=0.2) # 设置网格线的透明度

    return axes