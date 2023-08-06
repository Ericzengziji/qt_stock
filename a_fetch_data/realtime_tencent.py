#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file  : qt_stock --> realtime_tencent.py
@author: zengziji
@time  : 2023-08-06 15:37
@desc  ： 腾讯股票实时接口, http://qt.gtimg.cn/q=sh600036
"""
import requests


def get_realtime_msg(stock_area_code):
    """

    :param stock_area_code:
    :return: ['date', 'time', 'code', 'open', 'high', 'low', 'close', 'volume',
       'amount', 'adjustflag']
    """
    url = "http://qt.gtimg.cn/q=" + stock_area_code
    res = requests.get(url = url)
    # print(res.text)
    result_list = res.text.split("~")
    date_info = result_list[30]
    output_dict = {}
    output_dict["date"] = date_info[:4] + '-' + date_info[4:6] + '-' + date_info[6:8]
    output_dict["time"] = date_info[8:]
    output_dict["code"] = stock_area_code.replace("sh", "sh.").replace("sz", "sz.")
    output_dict["price"] = float(result_list[3])

    return output_dict


if __name__ == '__main__':
    stock_area_code = 'sh600036'
    output_dict = get_realtime_msg(stock_area_code)
    print(output_dict)