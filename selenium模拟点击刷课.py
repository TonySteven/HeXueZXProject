#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 4/20/22 10:48
# @Author  : StevenL
# @Email   : stevenl365404@gmail.com
# @File    : selenium模拟点击刷课.py


import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# 设置webdriver为chrome
driver = webdriver.Chrome()


def login(username, password):
    """
    模拟登录
    Args:
        username: 学号
        password: 密码

    Returns: void

    """
    driver.get('http://login.hexuezx.cn/?code=10445&type=3')

    # 等待直到可以点击登录按钮
    wait = WebDriverWait(driver, 10)
    submit = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'submitButtom')))

    # 并填入学号
    element_xh_input = driver.find_element(by=By.XPATH,
                                           value='//*[@id="pane-login"]/form/li[3]/div[2]/div/div/div[1]/input')
    element_xh_input.send_keys(username)

    # 找到密码input,并填入
    driver.find_element(by=By.XPATH, value='//*[@id="pane-login"]/form/li[4]/div[2]/div/div/div/input').send_keys(
        password)
    # 点击登录
    submit.click()

    now = datetime.datetime.now()
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
    print('login success! 登录成功')


def t2s(t):
    """

    Args:
        t: mm:ss

    Returns: 秒数

    """
    if ':' in t:
        m, s = t.strip().split(":")
        return int(m) * 60 + int(s)
    else:
        return ''


def watch_course(course_num):
    """
    模拟点击我的课程,进入课程页面
    Args:
        course_num: 课程编号,点击第几门课程

    Returns: void

    """
    time.sleep(3)

    # 等待直到可以点击我的课程按键
    wait = WebDriverWait(driver, 120)
    button_my_course = wait.until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/aside/div/div/ul/li[6]/div')))

    print('点击我的课程按键')

    button_my_course.click()

    # 等待直到可以点击进入学习按钮
    wait = WebDriverWait(driver, 120)
    button_into_course = wait.until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="pane-being"]/div/div[3]/table/tbody/tr[' + course_num + ']/td[11]/div/button')))

    button_into_course.click()
    print('点击进入按键')

    # 等待页面跳转
    time.sleep(9)
    print('等待页面跳转')

    # driver.find_element(by=By.XPATH,
    #                     value='//*[@id="pane-being"]/div/div[3]/table/tbody/tr[1]/td[11]/div/button').click()

    # 点击课程学习按钮
    driver.find_element(by=By.XPATH, value='//*[@id="app"]/section/aside/div/div/ul/li[4]/div').click()
    print('点击课程学习按钮')

    # 等待页面跳转
    time.sleep(6)
    print('等待页面跳转')

    # 看下总共有多少节课程,就循环多少次
    element = WebDriverWait(driver, 120).until(
        ec.presence_of_element_located((By.CLASS_NAME, "collapse_content_box"))
    )
    courses_size = len(driver.find_elements(by=By.CLASS_NAME, value='collapse_content_box'))
    print('总课程数:' + str(courses_size))
    # courses_size = len(driver.find_element(by=By.LINK_TEXT, value='视频').size)

    # 等待直到可以课程继续学习按钮
    wait = WebDriverWait(driver, 120)
    button_keep_learning = wait.until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="study_content"]/div[2]/div/div[2]/div[2]/div[1]/div')))

    button_keep_learning.click()
    print('点击继续学习按钮')

    # original_window = driver.current_window_handle
    # 关闭当前窗口, 只保留一个页面,好操作.
    driver.close()
    # switch_to_new_window(original_window)

    for i in range(courses_size):
        print('第' + str(i + 1) + '次开始课程学习')

        watch_course_loop()


def check_exists_by_xpath(xpath):
    try:
        driver.find_element(by=By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_tag_name(tag_name):
    try:
        driver.find_element(by=By.TAG_NAME, value=tag_name)
    except NoSuchElementException:
        return False
    return True


def switch_to_new_window(original_window):
    """
    切换到新的窗口
    Args:

    Returns: void

    """

    # 等待页面跳转
    wait = WebDriverWait(driver, 9)
    # Store the ID of the original window
    # Wait for the new window or tab
    wait.until(ec.number_of_windows_to_be(2))
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    # Wait for the new tab to finish loading content
    # wait.until(EC.title_is("SeleniumHQ Browser Automation"))
    # driver.switch_to.window('main')


def watch_course_loop():
    """
    模拟点击我的课程,进入课程页面 可以循环调用
    Returns: void

    """

    driver.switch_to.window(driver.window_handles[0])

    # 等待页面跳转
    global delay_time

    # 判断是否有视频
    if check_exists_by_tag_name('video'):
        if check_exists_by_xpath('//*[@id="vjs_video_3"]/div[4]/div[4]/span[2]'):

            # 聚焦下video,更好的获取视频时长.
            # driver.switch_to.frame(driver.find_element(by=By.TAG_NAME, value='video'))

            # 等待直到可以点击视频市按钮
            wait = WebDriverWait(driver, 120)
            button_video = wait.until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="vjs_video_3"]/div[4]/div[4]/span[2]')))
            button_video.click()

            # 点下静音键
            driver.find_element(by=By.XPATH, value='//*[@id="vjs_video_3"]/div[4]/div[1]/button').click()

            video_end_time_str = driver.find_element(by=By.XPATH,
                                                     value='//*[@id="vjs_video_3"]/div[4]/div[4]/span[2]').text
            while video_end_time_str == '':
                time.sleep(3)
                video_end_time_str = driver.find_element(by=By.XPATH,
                                                         value='//*[@id="vjs_video_3"]/div[4]/div[4]/span[2]').text
            # 获取视频时长
            video_end_time = t2s(video_end_time_str)

            # 获取现在已观看时长
            video_time_str = driver.find_element(by=By.XPATH,
                                                 value='//*[@id="vjs_video_3"]/div[4]/div[2]/span[2]').text
            while video_time_str == '':
                time.sleep(3)
                video_time_str = driver.find_element(by=By.XPATH,
                                                     value='//*[@id="vjs_video_3"]/div[4]/div[2]/span[2]').text

            # 获取现在已观看时长
            video_time = t2s(video_time_str)

            delay_time = int(int(video_end_time) - int(video_time)) + 6

            print('等待' + str(delay_time) + '秒')
            # time.sleep(delay_time)
            WebDriverWait(driver, delay_time)
            print('正在等待....')
            # time.sleep(3)
        else:
            print('获取视频时长获取失败!')
            time.sleep(3)

    # 如果是非视频,直接退出学习并确认
    # 等待直到可以点击退出学习按钮
    wait = WebDriverWait(driver, 120)
    button_exit_course = wait.until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/section/main/div/div[1]/div/div[1]/div/div[2]/div/div/button')))

    button_exit_course.click()

    # 等待直到可以点击确认退出学习按钮
    wait = WebDriverWait(driver, 120)
    button_exit_course_confirm = wait.until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/section/main/div/div[2]/div/div[3]/span/button[2]')))

    button_exit_course_confirm.click()

    # 等待直到可以课程继续学习按钮
    wait = WebDriverWait(driver, 120)
    button_keep_learning = wait.until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="study_content"]/div[2]/div/div[2]/div[2]/div[1]/div')))
    # 点击继续学习
    button_keep_learning.click()

    driver.close()


# 调用登陆函数
login('221100901130011', '050211')

# 调用看课函数,跳转到课程观看页面,先看第一门课程
watch_course('3')

# 关闭浏览器
print('======完成刷课=======')
driver.quit()
