from translate import Translator
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def translate(sentence):
    translator = Translator(from_lang="ZH", to_lang="EN-US")
    translation = translator.translate(sentence)
    return translation

def openBaiduFanYi(url):
    # 无可视化界面设置 #
    edge_options = Options()
    # 使用无头模式
    edge_options.add_argument('--headless')
    # 禁用GPU，防止无头模式出现莫名的BUG
    edge_options.add_argument('--disable-gpu')
    # 指定msedgedriver位置和无头模式的配置
    # browser = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe", options=edge_options)
    # 使用打开浏览器的方式
    browser = webdriver.Edge(r"D:\four2\Graduating Design\nlp\msedgedriver.exe", options=edge_options)
    # 打开百度翻译网页
    browser.get(url)
    return browser

def translate_baidu(sentence):
    browser = openBaiduFanYi("https://fanyi.baidu.com")
    tryCount = 5
    res = ""
    while tryCount > 0:
        try:
            input_baidu = browser.find_elements(By.ID, "baidu_translate_input")
            input_baidu[0].clear()
            input_baidu[0].send_keys(sentence)
            time.sleep(2)  # 等待2S后取回翻译结果
            res = browser.find_elements(By.XPATH, "//*[@class='ordinary-output target-output clearfix']")[0].text
            tryCount = 0
        except Exception as e:
            tryCount -= 1
    return res

def translate_youdao(sentence):
    browser = openBaiduFanYi("https://fanyi.youdao.com/index.html#/")
    tryCount = 5
    res = ""
    while tryCount > 0:
        try:
            input_youdao = browser.find_elements(By.ID, "js_fanyi_input")
            input_youdao[0].clear()
            input_youdao[0].send_keys(sentence)
            time.sleep(2)  # 等待2S后取回翻译结果
            res = browser.find_elements(By.XPATH, "//*[@id=\"js_fanyi_output_resultOutput\"]/p/span")[0].text
            tryCount = 0
        except Exception as e:
            tryCount -= 1
    return res

if __name__=="__main__":
    print(translate_baidu("好人一生平安"))