# -*- coding: utf-8 -*-
import time
import logging
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.common.exceptions import (NoSuchCookieException,
                                        NoSuchElementException,
                                        TimeoutException)


def log(LEVEL="loggin.INFO", *, filename="log.txt",filemode="w"):
    format = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] \
            - %(levelname)s: %(message)s")
    logger = logging.getLogger()
    logger.setLevel(LEVEL)
    # 文件handler
    fh = logging.FileHandler(filename="./logs/"+filename,
                             mode=filemode, encoding="utf-8")
    fh.setFormatter(format)
    fh.setLevel(logging.INFO)
    # 控制台handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(format)
    logger.addHandler(fh)
    logger.addHandler(ch)


def jw_login(username, password):
    log(logging.INFO, filename="gradeLog.txt",filemode="a")
    url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3a%2f%2fjw.cidp.edu.cn%2fLoginHandler.ashx"
    driver = webdriver.Chrome(executable_path=r"./chrome/chromedriver.exe")
    driver.get(url=url)
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_tag_name('button').click()
    driver.get(url="https://jw.cidp.edu.cn/Navigation/Default.htm")
    driver.get(
        url="https://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx")
    xueqi = driver.find_element_by_xpath("//input[@id='hfSemesterFramework']")
    chengji = driver.find_element_by_xpath(
        "//input[@id='hfAverageMarkFromClass']")
    xueqi = xueqi.get_attribute("value")
    chengji = chengji.get_attribute("value")
    driver.quit()
    return xueqi, chengji 

if __name__ == "__main__":
    jw_login("175043115", "Ygq520123456!")
