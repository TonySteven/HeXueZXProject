#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 4/20/22 10:48
# @Author  : StevenL
# @Email   : stevenl365404@gmail.com
# @File    : selenium模拟点击刷课.py
import datetime
import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from utils.utils import t2s

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


def watch_course(course_num):
    """
    模拟点击我的课程,进入课程页面
    Args:
        course_num: 课程编号,点击第几门课程

    Returns: void

    """

    # 点击页面上在线课程的课程学习按钮,等待直到可以点击进入学习按钮
    wait = WebDriverWait(driver, 120)
    button_into_course = wait.until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/section/main/div/div[1]/div[1]/div[2]/div/ul/li[' + course_num
             + ']/div[2]/div[2]/div[2]/button[1]')))

    button_into_course.click()
    print('点击进入按键')

    click_keep_learn()
    print('点击继续学习按钮')

    # driver.close()
    # 对焦到新页面,并关闭原窗口, 只保留一个页面,好操作.
    # switch_to_new_window(original_window)
    # switch_to_newest_window_and_close_original_window()
    # for i in range(courses_size):
    # 无限循环,直到手动关闭
    while True:
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


def switch_to_newest_window_and_close_original_window():
    """
    切换到新的窗口
    Args:

    Returns: void

    """
    original_window = driver.current_window_handle

    # 等待页面跳转
    wait = WebDriverWait(driver, 120)
    # Store the ID of the original window
    # Wait for the new window or tab
    wait.until(ec.number_of_windows_to_be(2))
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.close()
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
    time.sleep(6)

    # 创建一个全局变量,用来记录视频播放的时间
    global video_time

    # 判断是否有视频
    if check_exists_by_tag_name('video'):
        print('有视频,准备播放视频')
        button_video_string = '//*[@id="vjs_video_3"]/div[4]/div[4]/span[2]'
        if check_exists_by_xpath(button_video_string):

            # 聚焦下video,更好的获取视频时长.
            # driver.switch_to.frame(driver.find_element(by=By.TAG_NAME, value='video'))
            # move_to_element(to_element)鼠标移动到指定元素

            element_mute = WebDriverWait(driver, 20, 0.5).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, '//*[@id="vjs_video_3"]/div[4]/div[1]/button'))
            )
            if element_mute:
                button_mute = driver.find_element(by=By.XPATH, value='//*[@id="vjs_video_3"]/div[4]/div[1]/button')
                # 点击下静音键
                ActionChains(driver).move_to_element(button_mute).perform()
                # 点下静音键
                button_mute.click()
                print('点击静音按钮')

            # 等待直到可以点击视频时长按钮
            element_watch = WebDriverWait(driver, 20, 0.5).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, button_video_string))
            )
            if element_watch:
                driver.find_element(by=By.XPATH, value=button_video_string).click()
                print('点击视频时长按钮')

            video_end_time_str = driver.find_element(by=By.XPATH,
                                                     value=button_video_string).text
            while video_end_time_str == '':
                time.sleep(3)
                video_end_time_str = driver.find_element(by=By.XPATH,
                                                         value='//*[@id="vjs_video_3"]/div[4]/div[4]/span[2]').text
            # 获取视频时长
            video_end_time = t2s(video_end_time_str)
            print('视频时长:' + str(video_end_time))

            # 获取现在已观看时长
            video_time_str = driver.find_element(by=By.XPATH,
                                                 value='//*[@id="vjs_video_3"]/div[4]/div[2]/span[2]').text
            while video_time_str == '':
                time.sleep(3)
                video_time_str = driver.find_element(by=By.XPATH,
                                                     value='//*[@id="vjs_video_3"]/div[4]/div[2]/span[2]').text

            # 获取现在已观看时长
            video_time = t2s(video_time_str)
            print('现在已观看时长:' + str(video_time))

            delay_time = int(int(video_end_time) - int(video_time)) + 6

            print('等待' + str(delay_time) + '秒')

            print('正在等待....')
            # 等待视频播放完毕,并找到视频按钮
            delay_exit_leaning(delay_time)
        else:
            print('获取视频时长获取失败!')
            time.sleep(3)
    else:
        delay_exit_leaning(3)


def delay_exit_leaning(delay_second):
    """

    Returns: void

    """
    # 等待delay_second秒数
    time.sleep(delay_second)
    # 查看sleep是否结束
    print('等待完成....' + str(delay_second) + '秒')

    # # 如果是非视频,直接退出学习并确认,退出学习并确认.
    # driver.find_element(by=By.XPATH,
    #                     value='//*[@id="app"]/section/main/div/div[1]/div/div[1]/div/div[1]/div/div/button').click()
    # 20秒内，直到元素在页面中可定位，点击元素,否则抛出异常.
    element_exit = WebDriverWait(driver, 20, 0.5).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH, '//*[@class="outButton"]/button'))
    )
    if element_exit:
        driver.find_element(by=By.XPATH,
                            value='//*[@id="app"]/section/main/div/div[1]/div/div[1]/div/div[1]/div/div/button').click()

    # 点击确定按钮.
    element_yes = WebDriverWait(driver, 20, 0.5).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH, '//*[@id="app"]/section/main/div/div[2]/div/div[3]/span/button[2]'))
    )
    if element_yes:
        driver.find_element(by=By.XPATH,
                            value='//*[@id="app"]/section/main/div/div[2]/div/div[3]/span/button[2]').click()

    # 刷新方法 refresh
    # driver.refresh()
    # 等待页面跳转
    time.sleep(3)

    # 点击继续学习按钮,知道能点击位置
    click_keep_learn()


def click_keep_learn():
    try:
        # 等待直到可以课程继续学习按钮

        element_keep_learn = WebDriverWait(driver, 20, 0.5).until(
            EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, 'info_list_button'))
        )
        if element_keep_learn:
            # 点击继续学习按钮
            driver.find_element(by=By.CLASS_NAME,
                                value='info_list_button').click()
            print('点击继续学习按钮')
            switch_to_newest_window_and_close_original_window()
    except BaseException as e:
        # clean-up
        logging.exception('找不到继续学习按钮')
        raise e


def switch_to_window():
    handles = driver.window_handles
    for _ in handles:
        driver.switch_to.window('main')


# 调用登陆函数
login('221100901130011', '050211')

# 调用看课函数,跳转到课程观看页面,先看第一门课程
watch_course('1')

# 关闭浏览器
print('======完成刷课=======')
driver.quit()
