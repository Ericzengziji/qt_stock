#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file  : qt_stock --> fetch_data.py
@author: zengziji
@time  : 2023-07-30 21:38
@desc  ： 1、支持实时数据获取和历史数据获取 2、支持分钟、小时、天级数据获取 3、支持一次性返回和单次行行返回 4、多数据源情况返回dataframe的结构一致
"""
import datetime
import requests
import baostock as bs
import pandas as pd


class GetStockData(object):
    def __init__(self, stock_code, trade_day=None):
        """
        :param stock_code: 股票代码，如招商银行就是600036
        :param trade_day:  yyyy-MM-dd, 交易时间，默认当前日期，为了动态计算量比，方便回测
        """

        self.trada_day = trade_day if trade_day is not None else datetime.datetime.now().strftime('%Y-%m-%d')

        if ~isinstance(stock_code, str):
            stock_code = str(stock_code)
        if len(stock_code) != 6:
            print("please input stock_code which length is 6 !")
            raise ValueError("stock_code股票代码长度必须是6位数")
        else:
            if stock_code[:3] in ['600', '601', '603', '688']:
                self.stock_area_code = 'sh' + stock_code
                self.stock_code = stock_code
            elif stock_code[:2] in ['00', '30']:
                self.stock_area_code = 'sz' + stock_code
                self.stock_code = stock_code
            else:
                raise ValueError("无法识别stock_code归属上证指数还是深证指数，请检查股票代码前三位是否为600、601或000")

        print(self.stock_code, self.trada_day)

    def get_history_data_baostock(self, start_date, end_date, frequency="d"):
        """
        参考地址：http://baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3#.E8.8E.B7.E5.8F.96.E5.8E.86.E5.8F.B2A.E8.82.A1K.E7.BA.BF.E6.95.B0.E6.8D.AE
        :param start_date:开始日期（包含），格式“YYYY-MM-DD”，为空时取2015-01-01；
        :param end_date:结束日期（包含），格式“YYYY-MM-DD”，为空时取最近一个交易日；
        :param frequency:数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
        :return:

        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        fields：指示简称，支持多指标输入，以半角逗号分隔，填写内容作为返回类型的列。详细指标列表见历史行情指标参数章节，日线与分钟线参数不同。此参数不可为空；
        adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权。 BaoStock提供的是涨跌幅复权算法复权因子，具体介绍见：复权因子简介或者BaoStock复权因子简介。

        天级别参数：   date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST
        分级别参数：   date,time,code,open,high,low,close,volume,amount,adjustflag
        周月级别参数： date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        """
        lg = bs.login()
        # # 显示登陆返回信息
        # print('login respond error_code:' + lg.error_code)
        # print('login respond  error_msg:' + lg.error_msg)

        input_stockcode = self.stock_area_code.replace("sh", "sh.").replace("sz", "sz.")
        if frequency in ["d", "w", "m"]:
            input_feilds = "date,code,open,high,low,close,volume,amount,adjustflag"
        else:
            input_feilds = "date,time,code,open,high,low,close,volume,amount,adjustflag"


        res = bs.query_history_k_data_plus(input_stockcode,
                                          input_feilds,
                                          start_date=start_date, end_date=end_date,
                                          frequency=frequency, adjustflag="3")
        data_list = []
        if res.error_code != '0':
            print('query_history_k_data_plus respond error_code:' + res.error_code)
            print('query_history_k_data_plus respond  error_msg:' + res.error_msg)

        else:
            while res.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(res.get_row_data())
        bs.logout()

        result = pd.DataFrame(data_list, columns=res.fields)
        if frequency in ["d", "w", "m"]:
            result.insert(loc=1, column='time', value='093500')
        else:
            result['time'] = result['time'].apply(lambda x:x[8:14])

        # 更新数据类型
        for col in ["open","high","low","close","amount"]:
            if col in result.columns:
                result[col] = result[col].astype("float")
        for col in ["volume"]:
            if col in result.columns:
                result[col] = result[col].astype("int64")

        return result

    def get_history_5min_data(self, cover_day=1):
        """
        5分钟粒度的话，一天4小时交易时间，一天共计有 4*60/5=48 行记录
        参数：股票编号、分钟间隔（5、15、30、60）、均值（5、10、15、20、25）、查询个数点（最大值242,建议是48的倍数））
        注意开始的5个ma5值都是0

        :param cover_day:
        :return:
        """

        url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=5&ma=5&datalen=%d"%(self.stock_area_code, 48*cover_day)
        res = requests.get(url)
        res_data_list = eval(res.text)
        print(res_data_list)


    # def get_history_60min_data(self, cover_day=30):
    #     ##60分钟粒度的话，一个4小时交易时间，一天共计有 4 行记录
    #     ##（参数：股票编号、分钟间隔（5、15、30、60）、均值（5、10、15、20、25）、查询个数点（最大值242,建议是4的倍数））
    #     ##注意开始的5个ma5值都是0
    #     url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=60&ma=25&datalen=%d"%(self.stock_area_code, 4*cover_day)
    #     res = requests.get(url)
    #     res_data_list = eval(res.text)
    #     ##构建delete_sql
    #     begin_date = res_data_list[0]['day']
    #     end_date = res_data_list[-1]['day']
    #     delete_sql = """delete from stock_db.trade_60min_di where trade_date>='%s' and trade_date<='%s' and stock_code='%s';"""%(begin_date, end_date, self.stock_code)
    #     send_sql(sql=delete_sql, get_or_not=0)
    #
    #     ##构架sql插入的values
    #     insert_values_list = []
    #     col_name = ['stock_code', 'trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'ma_price25', 'ma_volume25']
    #     for per_data in res_data_list:
    #         tmp_list = list(per_data.values())
    #         ##添加股票代码
    #         tmp_list.insert(0, self.stock_code)
    #         delta = len(col_name) - len(tmp_list)
    #         for i in range(delta):
    #             tmp_list.append('0.0')
    #         # print(str(tuple(tmp_list)))
    #         insert_values_list.append(str(tuple(tmp_list)))
    #
    #     insert_sql = """insert into stock_db.trade_60min_di(%s) values %s;"""%(",".join(col_name), ",".join(insert_values_list))
    #     send_sql(sql=insert_sql, get_or_not=0)


if __name__ == '__main__':
    test = GetStockData(stock_code='600036')
    output_data = test.get_history_data_baostock(start_date='2023-07-26', end_date='2023-07-26', frequency="5")
