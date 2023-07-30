#### MySQL 字符串命令

```
PREPARE str_cmd FROM 'select acct_id from cash_quarter where stdate=? limit 1;';
set @stdate='2019Q1';
execute str_cmd using @stdate;
```

使用 PREPARE 的几个注意点： 

O：PREPARE stmt_name只能支持一个命令，不能多行命令

A：PREPARE stmt_name FROM preparable_stmt; 

预定义一个语句，并将它赋给 stmt_name ，stmt_name 是不区分大小写的。


B： 即使 preparable_stmt 语句中的 ? 所代表的是一个字符串，你也不需要将 ? 用引号包含起来。 

C： 如果新的 PREPARE 语句使用了一个已存在的 stmt_name ，那么原有的将被立即释放！ 即使这个新的 PREPARE 语句因为错误而不能被正确执行。 

D： PREPARE stmt_name 的作用域是当前客户端连接会话可见。 

E： 要释放一个预定义语句的资源，可以使用 DEALLOCATE PREPARE 句法。


F： EXECUTE stmt_name 句法中，如果 stmt_name 不存在，将会引发一个错误。 

G： 如果在终止客户端连接会话时，没有显式地调用 DEALLOCATE PREPARE 句法释放资源，服务器端会自己动释放它。 

H： 在预定义语句中，CREATE TABLE, DELETE, DO, INSERT, REPLACE, SELECT, SET, UPDATE, 和大部分的 SHOW 句法被支持。 

G： PREPARE 语句不可以用于存储过程，自定义函数！但从 MySQL 5.0.13 开始，它可以被用于存储过程.

 

月度表备份代码：

```
BEGIN
set @first_day=DATE_FORMAT(DATE_FORMAT(NOW(),'%y-%m-%d') - INTERVAL DAY(DATE_FORMAT(NOW(),'%y-%m-%d')) DAY,'%Y%m%d');
set @info_day=DATE_FORMAT((select date_add(create_time,interval -1 day) from qd.acct_info limit 1),'%Y%m%d');
set @table_name=concat('qd.acct_info',DATE_FORMAT(@info_day,'%Y%m'));


if @first_day=@info_day then 
	BEGIN
		set @drop_sql=concat('drop table if exists ',@table_name,';');
		set @create_sql=concat('create table ',@table_name,' like qd.acct_info;');
		set @insert_sql=concat('insert into ',@table_name,' select * from qd.acct_info;');
		PREPARE str_cmd FROM @drop_sql;
		execute str_cmd;
		DEALLOCATE PREPARE str_cmd;
		
		PREPARE str_cmd FROM @create_sql;
		execute str_cmd;
		DEALLOCATE PREPARE str_cmd;
		
		PREPARE str_cmd FROM @insert_sql;
		execute str_cmd;
		DEALLOCATE PREPARE str_cmd;

	END;
else
	select '月度备份表还没到时候~';
end if;

END
```

