# -*- coding: utf-8 -*-
import json
import time
import logging
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.common.exceptions import (NoSuchCookieException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options


def display_time(fun):
    def deco(*args, **kwargs):
        begin = time.time()
        re = fun(*args, **kwargs)
        end = time.time()
        print(fun.__name__, "函数耗时", (end-begin), "秒")
        return re
    return deco


def log(LEVEL="loggin.INFO", *, filename="log.txt", filemode="w"):
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


@display_time
def getDriver():
    browser_path = r"./chrome/chromedriver.exe"
    try:
        log(logging.INFO, filename="driverLog.txt")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(
            executable_path=browser_path, chrome_options=chrome_options)
        return driver
    except Exception:
        raise IOError("加载web驱动出错了")
        logging.info("加载web驱动出错了")


# 实验证明Phantoms内核跑的比chrome快
@display_time
def getDriver_Phantoms():
    browser_path = r"Phantoms/bin/phantomjs.exe"
    try:
        log(logging.INFO, filename="driverLog.txt")
        driver = webdriver.PhantomJS(executable_path=browser_path)
        return driver
    except Exception:
        raise IOError("加载web驱动出错了")
        logging.info("加载web驱动出错了")


@display_time
def getCookies(username, password):
    log(logging.INFO, filename="getCookiesLog.txt")
    url = "http://authserver.cidp.edu.cn/authserver/login?\
        service=http%3A%2F%2Fehall.cidp.edu.cn%2Flogin%3F\
        service%3Dhttp%3A%2F%2Fehall.cidp.edu.cn%2Fnew%2Findex.html"
    try:
        driver = getDriver_Phantoms()
        driver.get(url=url)
        driver.find_element_by_name('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_tag_name('button').click()
        cookies = driver.get_cookies()
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
            # print(cookie)
        driver.quit()
        return jar
    except TimeoutException:
        logging.info("请求超时，可能是教务处挂了")
    except NoSuchCookieException:
        logging.info("没有获取到Cookies")
    except NoSuchElementException:
        logging.info("没有找到元素")
    driver.quit()
    return False


@display_time
def login(url, username, password):
    try:
        jar = getCookies(username, password)
        res = requests.get(url=url, cookies=jar)
        res.text.encode("utf-8")
        res = res.text
        res = res.strip('[]')
        res = json.loads(res)
        print(type(res))
        return res
    except Exception:
        print("查询失败，请检查用户名和密码及网络！")


@display_time
def jw_login(username, password):
    log(logging.INFO, filename="gradeLog.txt", filemode="a")
    url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3a%2f%2fjw.cidp.edu.cn%2fLoginHandler.ashx"
    driver = getDriver_Phantoms()
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
