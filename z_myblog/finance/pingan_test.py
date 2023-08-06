"""
悲观做T法
原理：预计今日最低值，提前委托买入，于次日托管卖出。
原则：悲观 即对最低值要悲观，宁可无法买入也不尽量不能容忍过高买入
应用场景：该股票近期基本横盘或者上涨
"""
import requests
import json

stock_code = "sh601318"
url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=5&ma=5&datalen=1024"%stock_code



res = requests.get(url)
##temp = res.text.replace("high","'high'").replace("day","'day'").replace("open","'open'").replace("ma_volume5","'ma_volume5'").replace("low","'low'").replace("volume:","'volume':").replace("ma_price5","'ma_price5'").replace("close","'close'")

temp = res.text.replace("{","{'").replace("\",","\",'").replace(":\"","':\"").replace("e5","e5'").replace(",m",",'m")
data = eval(temp)

for index,row in enumerate(data):
    pass
