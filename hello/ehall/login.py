# -*- coding: utf-8 -*-
import json
import time
import logging
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


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
        return jar
    except Exception:
        return 501
    finally:
        driver.quit()


@display_time
def login(url, username, password):
    jar = getCookies(username, password)
    if jar is not int:
        res = requests.get(url=url, cookies=jar)
        res = res.text
        print(res)
        try:
            res = json.loads(res)
            return res
        except json.JSONDecodeError:
            return 503
    else:
        return jar


@display_time
def jw_driver(username, password):
    log(logging.INFO, filename="gradeLog.txt", filemode="a")
    url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3a%2f%2fjw.cidp.edu.cn%2fLoginHandler.ashx"
    try:
        driver = getDriver_Phantoms()
        driver.get(url=url)
        driver.find_element_by_name('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_tag_name('button').click()
        driver.get(url="https://jw.cidp.edu.cn/Navigation/Default.htm")
        if driver.title == "本科生教务管理系统":
            driver.quit()
            return 503
        else:
            return driver
    except NoSuchElementException:
        return 503
    except Exception:
        return 500


@display_time
def jw_login(username, password):
    try:
        driver = jw_driver(username, password)
        if driver is not int:
            driver.get(
                url="https://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx")
            xueqi = driver.find_element_by_xpath(
                "//input[@id='hfSemesterFramework']")
            chengji = driver.find_element_by_xpath(
                "//input[@id='hfAverageMarkFromClass']")
            xueqi = xueqi.get_attribute("value")
            chengji = chengji.get_attribute("value")
            return json.loads(xueqi), json.loads(chengji)
        else:
            return driver
    finally:
        driver.quit()


@display_time
def jw_get(username, password):
    try:
        driver = jw_driver(username, password)
        print(driver)
        if driver is not int:
            cookies = driver.get_cookies()
            print(cookies)
            driver.quit()
            jar = RequestsCookieJar()
            for cookie in cookies:
                jar.set(cookie['name'], cookie['value'])
            print(jar)
            se = requests.session()
            se.cookies.update(jar)
            data = {'action': 'getInfo'}
            res = se.post(
                url="https://jw.cidp.edu.cn/RegisterInfo/RegisterManageHandler.ashx", data=data)
            print(res.text)
            return json.loads(res.text)
        else:
            return driver
    finally:
       pass


def jw_get_photo(username, password):
    try:
        driver = jw_driver(username, password)
        print(driver)
        if type(driver) is not int:
            cookies = driver.get_cookies()
            print(cookies)
            driver.quit()
            jar = RequestsCookieJar()
            for cookie in cookies:
                jar.set(cookie['name'], cookie['value'])
            print(jar)
            se = requests.session()
            se.cookies.update(jar)
            res = se.get(url="https://jw.cidp.edu.cn/RegisterInfo/RegisterManageHandler.ashx?action=getPhoto")
            return res
        else:
            return driver
    finally:
        pass


@display_time
def clear_Data(xueqi, chengji):
    for year in xueqi:
        for i in year["List"]:
            gradeList = []
            for n in chengji:
                if int(i["SemesterId"]) == int(n["SemesterID"]):
                    gradeList.append(n)
            i.update({"gradeList": gradeList})
    return xueqi
