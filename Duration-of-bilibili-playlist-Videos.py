# -*- coding: utf-8 -*-
# Author: Jin Duosi
# @Time: 2024/11/15 11:11

## 自动爬取网页时长并累加计算
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def extract_time_components(time_string):
    # 定义正则表达式模式
    pattern = r"(?:(\d+):)?(\d{1,2}):(\d{1,2})"

    # 使用 re.match 查找匹配项
    match = re.match(pattern, time_string)

    if match:
        # 提取匹配的部分
        hour = match.group(1)
        minute = match.group(2)
        second = match.group(3)

        # 将小时转换为整数，如果没有小时部分，则默认为0
        hour = int(hour) if hour else 0
        minute = int(minute)
        second = int(second)

        return hour, minute, second
    else:
        raise ValueError("Invalid time format")


def add_time_to_seconds(hour, minute, second):
    total_seconds = hour * 3600 + minute * 60 + second
    return total_seconds

def seconds_to_hour_minute_second(seconds):
    hour = seconds // 3600
    minute = (seconds % 3600) // 60
    second = seconds % 60
    return hour, minute, second

browser = webdriver.Chrome()
browser.get('https://space.bilibili.com/629605267/channel/collectiondetail?sid=1751012')
time.sleep(3)

# class="length"
time_elem = browser.find_elements(By.CLASS_NAME, 'length')
# class="item cur" 或者Xpath
playlist_name_elem = browser.find_element(By.CSS_SELECTOR, '#page-collection-detail > div > div > div > div > div.breadcrumb > span')

total_playlist_seconds = 0

for i in time_elem:
    hour, minute, second = extract_time_components(i.text)
    total_seconds = add_time_to_seconds(hour, minute, second)
    total_playlist_seconds += total_seconds
    print(f"Time: {i.text} -> Hour: {hour}, Minute: {minute}, Second: {second}")
    print(f"时长: {total_seconds} 秒")
print(f"总时长: {total_playlist_seconds} 秒")


hour, minute, second = seconds_to_hour_minute_second(total_playlist_seconds)
print(f"{playlist_name_elem.text}   总时长: {hour}:{minute}:{second}")

browser.quit()





# # 测试时间字符串
# time_strings = ["1:32:23", "31:34","13:02"]
#
# for time_string in time_strings:
#     hour, minute, second = extract_time_components(time_string)
#     print(f"Time: {time_string} -> Hour: {hour}, Minute: {minute}, Second: {second}")
#     total_seconds = add_time_to_seconds(hour, minute, second)
#     print(f"Total seconds: {total_seconds}\n")
