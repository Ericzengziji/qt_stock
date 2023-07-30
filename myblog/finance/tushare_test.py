import tushare as ts

##print(ts.__version__)

token = """c37f56b018dd6425b82df01de1c729bd95cf44737b24d8a07601f0f5"""


pro = ts.pro_api(token)

df = pro.trade_cal(exchange='',start_date='20180901',end_date='20181001',
                   fields='exchange,cal_date,is_open,pretrade_date',
                   is_open='0')


#查询当前所有正常上市交易的股票列表
stock_name_list = pro.stock_basic(exchange='', list_status='L',
                       fields='ts_code,symbol,name,area,industry,list_date')

##正则表达式抽取目标
temp = stock_name_list[stock_name_list['name'].str.match('.+上.+')]
print(temp)


##获取历史某一天的数据，参数还可以是ts_code/start_date/end_date
##维度还可以是weekly/monthly
daily_data = pro.daily(trade_date='20180810')


