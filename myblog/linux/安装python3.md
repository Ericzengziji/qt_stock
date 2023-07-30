#### 首先安装依赖包

```
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
```

#### 下载

`wget -P /usr/my_software/ https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tar.xz`

#### 建立路径

```
mkdir /usr/local/python3 
```

#### 解压、安装

```
tar -xvJf  Python-3.6.6.tar.xz
cd Python-3.6.6
./configure --prefix=/usr/local/python3
make && make install
```

#### 添加软连接

`ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3`