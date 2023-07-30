参考地址：

[virtualenv](https://www.cnblogs.com/technologylife/p/6635631.html)

[requirements](https://www.cnblogs.com/hdulzt/articles/6924836.html)

### virtualenv

​	virtualenv 是一个创建隔绝的Python环境的工具。virtualenv创建一个包含所有必要的可执行文件的文件夹，用来使用Python工程所需的包

---

#### 安装

​	`pip install virtualenv`

---

#### virtualenvwrapper

​	鉴于virtualenv不便于对虚拟环境集中管理，所以推荐直接使用virtualenvwrapper。 virtualenvwrapper提供了一系列命令使得和虚拟环境工作变得便利。它把你所有的虚拟环境都放在一个地方。

```
pip install virtualenvwrapper
pip install virtualenvwrapper-win　　#Windows使用该命令
```

---

#### 创建虚拟环境(windows-cmd)　**mkvirtualenv**

`mkvirtualenv yourenviromentname` ，创建的新的虚拟环境总是“干净”的，不会带安装包

`workon` ，查看有什么虚拟环境

`workon yourenviromentname`，切入虚拟环境

`deactivate`，退出虚拟环境

`rmvirtualenv yourenviromentname`，删除虚拟环境

---

#### 快速生成requirement.txt的安装文件

​	进入虚拟环境后，pip freeze > requirements.txt

​	新环境安装对应包，pip install -r requirement.txt



---

### jupyter

#### 	坑

​	在安装jupyter时，如果一直是“正在连接服务器”或者'connecting the kernel'，那么就要安装tornado



#### 	虚拟环境中使用jupyter

​	在进入虚拟环境后记得先创建kernel，否则用的jupyter内核一直是默认的环境的，`python -m ipykernel install --name`



#### 发布

​	[参考链接](https://www.jianshu.com/p/08f276d48669?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation)

#### 步骤一：生成密钥

```python
from notebook.auth import passwd
passwd()
# 然后按照操作输入密码（这个密码是你以后登录notebook时使用的密码）
# 输入之后就会得到一串字符，要记住这个字符，后面会用到
```

#### 步骤二：生成配置文件

​	cmd命令行输入`jupyter notebook --generate-config`，生成jupyter_notebook_config.py

#### 步骤三：修改jupyter_notebook_config.py配置

```python
c.NotebookApp.ip = '*'
#设置可访问的ip为任意。
c.NotebookApp.open_browser = False
#设置默认不打开浏览器
c.NotebookApp.password = '第1步生成的密文'
c.NotebookApp.port = 8888
c.NotebookApp.notebook_dir = '/your/file/saved/path/'
```

