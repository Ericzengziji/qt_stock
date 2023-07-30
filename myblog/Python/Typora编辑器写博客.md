# Typora编辑器写博客

*Typora*中文版是一款免费的跨平台markdown编辑工具，功能强大，支持markdown的标准语法，还支持动态预览功能。

### 功能强大一：快捷键

+ Ctrl+Home：跳转至文首
+ Ctrl+End：跳转至末端
+ Ctrl+1/2/3/4：直接编辑标题，传统为###
+ Ctrl+/：切换编辑模式，调整格式的时候常用到源码模式
+ Ctrl+B：加粗当前的单词
+ Ctrl+shift+c：复制为markdown源码，**方便搬到网上**
+ Ctrl+shift+D：删除当前词
+ Ctrl+T：插入表格
+ 其他尽量好留markdown原编辑模式吧

---

### 功能强大二：fu图片的引用

+ Typora本身只能支持本地文件的引用，但这样把文章内容发布到另外一台服务器后会造成图片无法查看的问题，因此需要把图片上传到某个可以远程访问的地方，***[fu](https://github.com/klesh/fu/releases?mt=8&uo=4&ct=appcards)***这一工具很好的补充了windows环境下的图片上传功能，macos用户可以用iPic
+ windows可以下载 ***[fu](https://github.com/klesh/fu/releases?mt=8&uo=4&ct=appcards)***，打开应用后，复制图片，右键点击fu图标，点击最上面的upload即可复制对应的markdown超链接

![pic1](https://i.loli.net/2019/02/21/5c6e5389a5dbb.png)

  <center>对应复制出来的链接为：`![](https://i.loli.net/2019/02/21/5c6e5389a5dbb.png)`</center>

+ 需要注意的是图片的命名**不得含有中文**

  ---

### 功能强大三：表格

传统markdown写表格非常麻烦，如下:

源码：

```markdown
| 一个普通标题 | 一个普通标题 | 一个普通标题 |
| ------ | ------ | ------ |
| 短文本 | 中等文本 | 稍微长一点的文本 |
| 稍微长一点的文本 | 短文本 | 中等文本 |
```

效果：

| 左对齐标题       | 右对齐标题 |   居中对齐标题   |
| :--------------- | ---------: | :--------------: |
| 短文本           |   中等文本 | 稍微长一点的文本 |
| 稍微长一点的文本 |     短文本 |     中等文本     |

**Typora支持直接复制粘贴表格（excel）或者Ctrl+T插入表格**


| 字段名  | 中文名 |   字段类型   |
| :-----: | :----: | :----------: |
|  cdate  |  日期  |     date     |
|   uid   | 用户ID | varchar(200) |
| account | 账号名 | varchar(100) |

