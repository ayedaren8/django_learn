# -*- coding: utf-8 -*-
import json
import logging
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.common.exceptions import (NoSuchCookieException,
                                        NoSuchElementException,
                                        TimeoutException)


def log(LEVEL="loggin.INFO", *, filename="log.txt"):
    format = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] \
            - %(levelname)s: %(message)s")
    logger = logging.getLogger()
    logger.setLevel(LEVEL)
    # 文件handler
    fh = logging.FileHandler(filename="./logs/"+filename,
                             mode="w", encoding="utf-8")
    fh.setFormatter(format)
    fh.setLevel(logging.INFO)
    # 控制台handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(format)
    logger.addHandler(fh)
    logger.addHandler(ch)


def getDriver():
    browser_path = r"./chrome/chromedriver.exe"
    try:
        log(logging.INFO, filename="Log.txt")
        driver = webdriver.Chrome(executable_path=browser_path)
        return driver
    except Exception:
        raise IOError("加载web驱动出错了")


def getCookies(username, password):
    log(logging.INFO, filename="getCookiesLog.txt")
    url = "http://authserver.cidp.edu.cn/authserver/login?\
        service=http%3A%2F%2Fehall.cidp.edu.cn%2Flogin%3F\
        service%3Dhttp%3A%2F%2Fehall.cidp.edu.cn%2Fnew%2Findex.html"
    try:
        driver = webdriver.Chrome(executable_path=r"./chrome/chromedriver.exe")
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


def login(url, username, password):
    try:
        jar = getCookies(username, password)
        res = requests.get(url=url, cookies=jar)
        print("内部", res.text)
        res.text.encode("utf-8")
        res = res.text.strip('[]')
        res = json.loads(res)
        print(type(res))
        return res
    except Exception:
        print("查询失败，请检查用户名和密码及网络！")


def jw_login(username, password):
    log(logging.INFO, filename="gradeLog.txt", filemode="a")
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
