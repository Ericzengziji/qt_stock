import pywinauto
import time
from recognize_yzm import baidu_image_to_word
import time

def all_number(input_str):
    g = ['1','2','3','4','5','6','7','8','9','0']
    temp = 0
    for i in input_str:
        if i in g:
            temp += 1
        else:
            temp -= 4
    return temp

class StockTrader():
    def __init__(self,exe_path = r'D:\wlzq\xiadan.exe'):
        """打开下单程序"""
        ##打开下单程序
        self.app = pywinauto.Application().start(exe_path)

        ##获取最上层的window
        ##win = app.top_window()
        main_win = self.app.window(title="用户登录", class_name="#32770")##这个是根据win.print_control_identifiers()来的
        ##main_win.print_control_identifiers()

        account = '80194168'
        password = '365869'
        image_path = 'yanzhengma.jpg'
        ##账户控件定位
        main_win.window(title="80194168", class_name="Edit").set_text(account)
        ##交易密码的控件ID为000003F4,不知道为什么要写五个零要改写成0x
        main_win.window(control_id=0x3F4, class_name="Edit").set_text(password)
        ##验证码控件定位+截图保存，其截图原理是根据坐标来的，所以验证不能被挡住，注意要先pip install Pillow
        image_object = main_win.child_window(control_id=0x5DB, class_name="Static")
        image_object.capture_as_image().save(image_path)

        ##百度接口识别图像数字
        yzm,probability,res = baidu_image_to_word(image_path)

        ##初始化验证码识别精度
        count_max=10;count=0
        while (probability<0.99 and count<count_max) or all_number(yzm)!=4:
            ##切换验证码
            image_object.click();time.sleep(1)
            image_object.capture_as_image().save(image_path)
            count += 1
            yzm,probability,res = baidu_image_to_word(image_path)
            print(yzm,probability,all_number(yzm))

        ##验证码控件定位
        main_win.window(control_id=0x3EB, class_name="Edit").set_text(yzm);time.sleep(1)
        main_win.child_window(title="确定(&Y)", class_name="Button").click()
        main_win.child_window(title="确定(&Y)", class_name="Button").click()
        time.sleep(5)
        self.win = self.app.top_window()

    def buy(self,stock_id,price,num):
        """ 买入 """
        time.sleep(1)
        self.win.type_keys('{F1}')
        time.sleep(1)
        self.win.window(control_id=0x408, class_name="Edit").set_text(str(stock_id))
        self.win.window(control_id=0x409, class_name="Edit").set_text(str(price))
        self.win.window(control_id=0x40A, class_name="Edit").set_text(str(num))
        self.win.child_window(title="买入[B]", class_name="Button").click();time.sleep(0.5)
        self.app.top_window().child_window(title="是(&Y)", class_name="Button").click();time.sleep(0.5)
        self.app.top_window().child_window(title="确定", class_name="Button").click()

    def sale(self,stock_id,price,num):
        """ 卖出 """
        time.sleep(1)
        self.win.type_keys('{F2}')
        time.sleep(1)
        self.win.window(control_id=0x408, class_name="Edit").set_text(str(stock_id))
        self.win.window(control_id=0x409, class_name="Edit").set_text(str(price))
        self.win.window(control_id=0x40A, class_name="Edit").set_text(str(num))
        self.win.child_window(title="卖出[S]", class_name="Button").click();time.sleep(0.5)
        self.app.top_window().child_window(title="是(&Y)", class_name="Button").click();time.sleep(0.5)
        
        self.app.top_window().child_window(title="确定", class_name="Button").click()
        

    def take_back(self,stock_id,back_type='buy'):
        """ 卖出 """
        time.sleep(1)
        self.win.type_keys('{F3}')
        time.sleep(1)
        self.win.window(control_id=0xD14, class_name="Edit").set_text(str(stock_id))
        self.app.top_window().child_window(title="查询代码", class_name="Button").click();time.sleep(0.5)
        if back_type=='buy':
            self.app.top_window().child_window(title="撤买(X)", class_name="Button").click();
        elif back_type=='sale':
            self.app.top_window().child_window(title="撤卖(C)", class_name="Button").click();

        self.app.top_window().child_window(title="是(&Y)", class_name="Button").click();time.sleep(0.5)
        

temp = StockTrader()

##买入,设置股票代码,买入价格以及数量
temp.buy(stock_id=600030,price=19.5,num=100)

##撤单 可选择撤回买入还是卖出
##temp.take_back(stock_id=600030,back_type='buy')

