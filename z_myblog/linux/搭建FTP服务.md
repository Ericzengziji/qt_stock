	FTP 是File Transfer Protocol（文件传输协议）的英文简称，而中文简称为“文传协议”。用于Internet上的控制文件的双向传输

##### OS

CentOS7

##### 查看是否安装

`ftp rpm -qa | grep vsftpd`

##### 安装

`yum -y install vsftpd`

##### 启动 

`service vsftpd start`

##### 关闭 

`service vsftpd stop`

##### 开机自启

`chkconfig vsftpd on`

##### 配置文件

`vi /etc/vsftpd/vsftpd.conf`

具体配置说明，请自行百度，可以设置黑白名单、操作权限等

##### 取消匿名登录 

`anonymous_enable=NO`



##### 注意事项：

* 默认情况下，ftp的访客名单=系统用户，所以当用户用linux系统账户密码登录FTP后，就会访问到对应系统用户的目录/home/user_name*

+ 使用匿名登入时，所登入的目录。默认值为/var/ftp。注意ftp目录不能是777的权限属性，即匿名用户的家目录不能有777的权限
  anon_root=/var/ftp

##### 其他

[windows如何访问ftp服务器](<https://jingyan.baidu.com/article/95c9d20d533a0fec4e7561d4.html>)

[linux如何访问ftp服务器](<https://www.cnblogs.com/juandx/p/3998418.html>)

linux访问下载文件夹是可以通过wget进行

wget -P file_dir ftp://user_name:passwd@ip:port/file_name

