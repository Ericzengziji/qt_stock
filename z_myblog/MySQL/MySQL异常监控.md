#### 背景

​	109mysql开放了事件权限给各分，其好处是方便各分数据库使用人员按计划执行相关查询sql脚本，但同时也存在风险，风险主要是源自于事件设计不够规范（如锁表、进程卡死、计算时长多长等），如下图。

![](https://i.loli.net/2019/03/19/5c908dfbf2576.jpg)



#### 解决方案

​	传统解决方案是直接全部杀死 运行时长>时长阈值 的进程，但有些耗时长的进程是存在的，不好评估时长的阈值。

​	新解决方案：在mysql设置事件检测后台进程运行情况，根据运行时间和状态初步判断是否异常，然后触发http请求到直销数据中心服务号-度小秘，由度小秘发送异常进程给到相关DBA，然后**DBA根据情况选择性地杀死进程**。查询代码和流程设计如下图

```
select ID as 异常进程ID,USER,TIME,STATE,LEFT(INFO,20) as INFO
from information_schema.`PROCESSLIST`
where (command!='sleep' and time>3600 and info is not null) or state='waiting for table metadata lock '
order by TIME desc;
```



![](https://i.loli.net/2019/03/19/5c9093d831b98.png)

#### 方案展示

![](https://i.loli.net/2019/03/19/5c909fb94c270.jpg)