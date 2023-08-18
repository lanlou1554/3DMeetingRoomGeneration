import re
import time
 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
 
 
def openBaiduFanYi():
    # 无可视化界面设置 #
    edge_options = Options()
    # 使用无头模式
    edge_options.add_argument('--headless')
    # 禁用GPU，防止无头模式出现莫名的BUG
    edge_options.add_argument('--disable-gpu')
    # 指定msedgedriver位置和无头模式的配置
    # browser = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe", options=edge_options)
    # 使用打开浏览器的方式
    browser = webdriver.Edge("msedgedriver.exe", options=edge_options)
    # 打开百度翻译网页
    browser.get("https://fanyi.baidu.com")
    return browser
 
# 翻译测试
def trans_test(text):
    browser = openBaiduFanYi()
    input_baidu = browser.find_elements(By.ID, "baidu_translate_input")
    input_baidu[0].clear()
    input_baidu[0].send_keys(text)
    time.sleep(2) # 等待2S后取回翻译结果
    res = browser.find_elements(By.XPATH, "//*[@class='ordinary-output target-output clearfix']")[0].text
    print(res)

 
 
trans_test("外面有三圈椅子，里面有两圈椅子。")
# xlrd包高版本不支持读取xlsx，此处使用的时1.2.0版本
# transExcel("C:\TEST.XLS","C:\翻译TEST.XLS")