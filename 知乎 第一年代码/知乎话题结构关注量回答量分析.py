# coding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver.common.by import By

url = ('https://www.zhihu.com/topic/19776749/top-answers')

driver = webdriver.Chrome(executable_path=r"D:\yingyong\chromedriver.exe")
driver.maximize_window()
driver.get(url)
time.sleep(5)

# a = driver.find_element(By.CLASS_NAME, "Button Modal-closeButton Button--plain")      # 定位关闭登录页面按钮
# a.click()                           # 点击按钮
js = 'document.getElementByClass("Button Modal-closeButton Button--plain").click();'
driver.execute_script(js)



all_window_height =  []                        # 创建一个列表，用于记录每一次拖动滚动条后页面的最大高度
all_window_height.append(driver.execute_script("return document.body.scrollHeight;"))         #当前页面的最大高度加入列表
while True:
    driver.execute_script("scroll(0,100000)")      # 执行拖动滚动条操作
    time.sleep(3)
    check_height = driver.execute_script("return document.body.scrollHeight;")
    if check_height == all_window_height[-1]:        # 判断拖动滚动条后的最大高度与上一次的最大高度的大小，相等表明到了最底部
        break
    else:
        all_window_height.append(check_height)            # 如果不相等，将当前页面最大高度加入列表。

data = driver.page_source
soup = BeautifulSoup(data, 'lxml')
grades = soup.find_all(class_="ContentItem AnswerItem")
for grade in grades:
    print(grade)


# for url in urls:
#     print ("正在访问{}".format(url))
#     driver.get(url)
#     data = driver.page_source
#     soup = BeautifulSoup(data, 'lxml')
#     grades = soup.find_all(class_="ContentItem AnswerItem")
#     for grade in grades:
#         print(grade)
        # if '<td>' in str(grade):
        #     print(grade.get_text())
