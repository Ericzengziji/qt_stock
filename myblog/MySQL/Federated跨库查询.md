#### Federated

+ federated是mysql的储存引擎之一，默认是不开启的，开启后可支持远程mysql访问
+ 注意配置文件my.cnf(linux)或my.ini(windows)要添加federated，即开启federate服务
+ 在mysql建立与目标**表结构一致**且**engine为federated**的表即可，代码如下
```
CREATE TABLE federated_table (

    id     int(20) NOT NULL auto_increment,

    name   varchar(32) NOT NULL default '',

    other  int(20) NOT NULL default '0',

    PRIMARY KEY  (id),

    KEY name (name),

    KEY other_key (other)

) ENGINE=FEDERATED CONNECTION='mysql://user:password@remote_host:port/db_fed/test_table';
```