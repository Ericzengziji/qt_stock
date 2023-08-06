#coding=utf8
from PIL import Image
from PIL import ImageEnhance
from aip import AipOcr
import os


def baidu_image_to_word(image_path):
    """ 你的 APPID AK SK """
    APP_ID = '14364432'
    API_KEY = 'jgopMYaecGeGgaBr2EYWKNDZ'
    SECRET_KEY = 'TnpKrHyyc3IgrGw2L5ZzKRiY9F2seCSk'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    with open(image_path, 'rb') as fp:
        image = fp.read()


    """ 调用通用文字识别, 图片参数为本地图片 """
    client.basicGeneral(image);

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "ENG"
    options["detect_direction"] = "true"#是否检测图像朝向，默认不检测，即：false
    ##options["detect_language"] = "true"#是否检测语言，默认不检测
    options["probability"] = "true"#是否返回识别结果中每一行的置信度

    """ 带参数调用通用文字识别, 图片参数为本地图片 """

    res = client.basicAccurate(image, options)#通用文字识别(高精度版),普通版是client.basicGeneral(image, options);
    ##""" 调用通用文字识别, 图片参数为远程url图片 """
    ##url = "https//www.x.com/sample.jpg"
    ##client.basicGeneralUrl(url,options);
    try:
        guess = res['words_result'][0]['words']
        probability = res['words_result'][0]['probability']['average']
    except:
        print("识别失败，将置信度归为0，文字为空")
        guess = '';probability=0;

    return guess,probability,res
