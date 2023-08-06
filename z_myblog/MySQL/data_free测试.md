未清理时2019-06-21 18：34：00

cash_encrp.cash_total_daily

数据长度:9.88 GB

索引长度:5.20 GB

数据空闲:3.53 GB



测试1-单表查询

select stdate,sum(cash)
from cash_encrp.cash_total_daily
where product_code=1
group by stdate

耗时：31s



测试2-关联查询

select b.op_unit_name1,sum(cash)
from cash_encrp.cash_total_daily a
join zhixiao_acct.acct_info b
on a.acct_id=b.acct_id
where product_code=1 and a.stdate>='20190101'
group by b.op_unit_name1

耗时：46s







清理后时2019-06-21 09：03：00

cash_encrp.cash_total_daily

数据长度:9.92 GB

索引长度:5.28 GB

数据空闲:7.00 MB





测试1-单表查询

select stdate,sum(cash)
from cash_encrp.cash_total_daily
where product_code=1
group by stdate

耗时：31s



测试2-关联查询

select b.op_unit_name1,sum(cash)
from cash_encrp.cash_total_daily a
join zhixiao_acct.acct_info b
on a.acct_id=b.acct_id
where product_code=1 and a.stdate>='20190101'
group by b.op_unit_name1

耗时：55s



实验一结果：data_free空间减少了，但查询效率上并没有提升





