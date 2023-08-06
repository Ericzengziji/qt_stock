from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.application import MIMEApplication
from pandas import ExcelWriter

def convert_content(mail_content,dfs=None,table_title=None):
##    style格式："{'column_name':'style=background:#FFFF00;font-size:15px;color:#B3BBFF;','column_name2':'style=background:#FFFF00'}"
    
    content = """
<html>
<head>
    <meta charset="utf-8" />
    <title>邮件内容</title>
    <style type="text/css">
        body {
            margin-left: 0px;
            margin-top: 0px;
            margin-right: 0px;
            margin-bottom: 0px;
            font-family: "Microsoft YaHei",微软雅黑;
            background-position: right bottom;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        table {
            background: #ddd;
            width: 100%;
            border-spacing: 0;
            border-collapse: collapse;
            font-size: 12px;
        }
            table thead tr {
                background: #B3BBFF;
            }

            table tbody tr {
                background: #FFF;
            }

            table th, td {
                border: solid 1px #ddd;
                border-bottom: 1px solid #ddd;
                text-align: left;
                padding: 8px;
                line-height: 1.42857143;
                vertical-align: top;
                border-top: 1px solid #ddd;
            }
            .title {
            color: #777;
            text-align: left;
            font-weight: bold;
            font-size: 13px;
        }
    </style>
</head>
<body>
"""
    mail_content = mail_content.replace('\n','</br>')
    content +=""" <p><font color="#000000" font-size="28px">%s</font></p>"""%mail_content

    ##多少个df就多少个检验表
    if dfs is not None:
        k=0
        for df in dfs:
            df = df.fillna('')
            if 'css_style' in df.columns:
                style = list(df['css_style'])
                del df['css_style']
            else:
                style= []
                for i in range(0,len(df)):
                    style.append('{}')
            
            ##表标题
            if table_title==None:
                content +="""<div class="title">框架查询表%d</div><table>"""
                ##content += """<table><caption>框架查询表%d</caption>"""%(k+1)
            else:
                content += """<div class="title">%s</div><table>"""%table_title[k]
                ##content += """<table><caption>%s</caption>"""%table_title[k]
            k+=1

            ##表头
            content += """<thead><tr>"""
            for i in df.columns:
                content += '<th>%s</th>'%i
            content += '</tr><t/head>'

            ##表内容
            content += """<tbody><tr>"""
            for index, row in df.iterrows():
                for col in df.columns:
                    value = row[col]
                    try:
                        value_style = eval(style[index])
                    except:
                        value_style = {}
                        
                    if col in value_style.keys():
                        content += '<td %s>%s</td>'%(value_style[col],value)
                    else:
                        content += '<td>%s</td>'%value
                content += '</tr>'
            content += '</tbody></table><br>'

    content +="""<p><font color="#0000FF" font-size="38px"><strong>By 直销数据中心-度小秘</strong></font></p></body></html>"""
##    fh = open(r'D:\DXM\email.txt', 'w', encoding='utf-8')
##    fh.write(content)
##    fh.close()
    all_text = MIMEText(content,_subtype='html',_charset='utf-8')
    return all_text

def baidu_email(to_who,mail_title,mail_content,df=None,table_title=None,attach=None,cc=None):
    #百度邮箱smtp服务器
    host_server = 'email.baidu.com'
    smtpPort='25'
    sender = 'dxm@baidu.com'

    ##登录名
    username = 'dxm'
    ##登陆密码
    password = 'Mi&EWg@eQQ'
    #收件人邮箱
    ##to_who = 'zengziji@sz.baidu.com'

    #邮件的正文内容
    ##mail_content = '你好，现在在进行一项用python登录qq邮箱发邮件的测试\n 啊咧'
    #邮件标题
    ##mail_title = 'zzj的邮件'

    #tls登录
    smtp = smtplib.SMTP(host_server,smtpPort) 
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.ehlo()  
    smtp.starttls()  
    smtp.ehlo()  
    smtp.login(username,password) 

    # 构造MIMEMultipart对象做为根容器
    main_msg = MIMEMultipart()
    ##正文内容
    msg = convert_content(mail_content,df,table_title)
    main_msg.attach(msg)
    
    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    if attach is not None:
        #保存成excel
        writer = ExcelWriter('output.xlsx')
        for index,data in enumerate(attach):
            data.to_excel(writer,'Sheet%d'%(index+1),index=False)
        writer.save()
        xlsxpart = MIMEApplication(open('output.xlsx', 'rb').read())
        basename = '渠道日报附件1.xlsx'
        xlsxpart.add_header('Content-Disposition', 'attachment', filename=('gbk', '', basename))
        main_msg.attach(xlsxpart)

    main_msg["Subject"] = Header(mail_title, 'utf-8')
    main_msg["From"] = sender
    main_msg["To"] = to_who
    main_msg["CC"] = cc
    smtp.sendmail(sender,to_who.split(',') ,main_msg.as_string())
    smtp.quit()
