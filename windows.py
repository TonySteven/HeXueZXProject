#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 4/21/22 12:28
# @Author  : StevenL
# @Email   : stevenl365404@gmail.com
# @File    : windows.py

import time

from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()  # 窗口最大化
driver.get('https://www.baidu.com')  # 在当前浏览器中访问百度
# 新开一个窗口，通过执行new一个窗口
new = 'window.open("https://www.sogou.com");'
driver.execute_script(new)

print(driver.current_window_handle)  # 输出当前窗口句柄（百度）
handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
print(handles)  # 输出句柄集合

for handle in handles:  # 切换窗口（切换到搜狗）
    if handle != driver.current_window_handle:
        print('switch to ', handle)
        driver.switch_to.window(handle)
        print(driver.current_window_handle)  # 输出当前窗口句柄（搜狗）
        break

time.sleep(2)
driver.close()  # 关闭当前窗口（搜狗）
time.sleep(2)
driver.switch_to.window(handles[0])  # 切换回百度窗口
