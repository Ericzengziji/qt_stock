```python
from ftplib import FTP
ftp=FTP() #设置变量
ip = '172.xx.xxx.xx'
port = 2121
ftp.connect(ip,port) #连接的ftp sever和端口
ftp.login('usera','12345')#连接的用户名，密码如果匿名登录则用空串代替即可
#在FTP连接中切换当前目录 
#path = "/home1/ftproot/ybmftp/testupg/payment"
#ftp.cwd(path) 
ftp.dir()##打印当前路径
filename='vsftpd-3.0.3.tar.gz' #需要下载的文件 
save_file =open(filename,"wb")#以写模式在本地打开文件
ftp.retrbinary('RETR ' +filename,save_file.write) #接收服务器上文件并写入本地文件
save_file.close()
ftp.close() #退出ftp 
```



