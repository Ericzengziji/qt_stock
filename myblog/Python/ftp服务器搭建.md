#### 关于FTP

​	 FTP是File Transfer Protocol(文件传输协议)。FTP服务器（File Transfer Protocol Server）是在互联网上提供文件存储和访问服务的计算机，它们依照FTP协议提供服务。

​	FTP是用来在两台计算机之间传输文件,是Internet中应用非常广泛的服务之一。它可根据实际需要设置各用户的使用权限,同时还具有跨平台的特性,即在UNIX、Linux和Windows等操作系统中都可实现FTP客户端和服务器,相互之间可跨平台进行文件的传输。因此,FTP服务是网络中经常采用的资源共享方式之一。



#### 通过python搭建ftp服务器

##### ftpserver.pyw

```python
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import settings
import logging

def ftp_server():
    #实例化虚拟用户，这是FTP验证首要条件
    authorizer = DummyAuthorizer()
    
    #添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限)
    ##权限方面: 读权限:e-改变文件目录 l-列出文件 r-从服务器接收文件
    ##写权限:a-文件上传 d-删除文件 f-文件重命名 m-创建文件 w-写权限 M-文件传输模式
    authorizer.add_user('xxxxx', 'xxxxx', 'xxxxx', perm='elradfmw')
    #添加匿名用户 只需要路径
    if settings.enable_anonymous == 'on':
        authorizer.add_anonymous(settings.anonymous_path)
    
    #下载上传速度设置
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = settings.max_download
    dtp_handler.write_limit = settings.max_upload

    #初始化ftp句柄
    handler = FTPHandler
    handler.authorizer = authorizer

    #日志记录
    if settings.enable_logging == 'on':
        logging.basicConfig(filename=settings.loging_name, level=logging.INFO)

    #欢迎信息
    handler.banner = settings.welcome_msg
    
    #添加被动端口范围
    handler.passive_ports = range(settings.passive_ports[0], settings.passive_ports[1])

    #监听ip 和 端口
    server = FTPServer((settings.ip, settings.port), handler)
    
    #最大连接数
    server.max_cons = settings.max_cons
    server.max_cons_per_ip = settings.max_per_ip
    
    #开始服务
    print('开始服务')
    server.serve_forever()

if __name__ == "__main__":
    ftp_server()

```

##### setting.py

```python
ip = 'xxxxxxx'#本机ip地址
port = '2121'

#上传速度  300kb/s
max_upload = 300 * 1024

#下载速度 300kb/s
max_download = 300 * 1024

#最大连接数
max_cons = 150

#最多IP数
max_per_ip = 10

#被动端口范围，注意被动端口数量要比最大IP数多，否则可能出现无法连接的情况
passive_ports = (2000, 2200)

#是否开启匿名访问 on|off
enable_anonymous = 'off'
#匿名用户目录
anonymous_path = r'D:\ftp\conf'

#是否开启日志 on|off
enable_logging = 'off'
#日志文件
loging_name = 'pyftp.log'

#欢迎信息
welcome_msg = 'Welcome to ftp'
```



[windows如何访问ftp服务器](<https://jingyan.baidu.com/article/95c9d20d533a0fec4e7561d4.html>)

[windows如何设置开启启动py脚本](https://www.jianshu.com/p/d39e71c18d63)

