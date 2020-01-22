# -*- coding: utf-8 -*-
import json
import logging
import requests
from requests.cookies import RequestsCookieJar
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchCookieException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def log(LEVEL="loggin.INFO", *, filename="log.txt"):
    format = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    logger = logging.getLogger()
    logger.setLevel(LEVEL)
    # 文件handler
    fh = logging.FileHandler(filename="./logs/"+filename,
                             mode="a", encoding="utf-8")
    fh.setFormatter(format)
    fh.setLevel(logging.INFO)
    # 控制台handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(format)
    logger.addHandler(fh)
    logger.addHandler(ch)


def getCookies(username, password):
    log(logging.INFO, filename="getCookiesLog.txt")
    url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3A%2F%2Fehall.cidp.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cidp.edu.cn%2Fnew%2Findex.html"
    try:
        driver = webdriver.PhantomJS(
            executable_path=r'./Phantoms/bin/phantomjs.exe')
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


def jw_login(url, username, password):
    log(logging.INFO, filename="getCookiesLog.txt")
    url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3A%2F%2Fehall.cidp.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cidp.edu.cn%2Fnew%2Findex.html"
    try:
        driver = webdriver.PhantomJS(
            executable_path=r'./Phantoms/bin/phantomjs.exe')
        driver.get(url=url)
        driver.find_element_by_name('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_tag_name('button').click()
        cookies = driver.get_cookies()
        driver.get("http://www.xxxxx.com/loading")
        try:
            # 页面一直循环，直到 id="myDynamicElement" 出现
            element = WebDriverWait(driver,"""  """ 10).until(
                EC.presence_of_element_located((By.ID, "myDynamicElement"))
            )
        finally:
            driver.quit()
    except TimeoutException:
        logging.info("请求超时，可能是教务处挂了")
    except NoSuchCookieException:
        logging.info("没有获取到Cookies")
    except NoSuchElementException:
        logging.info("没有找到元素")
    driver.quit()
    return False
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
               }

    jw_url = "https://jw.cidp.edu.cn/Navigation/Default.htm"
    jar = getCookies(username, password)
    res = requests.get(url=jw_url, cookies=jar)
    cookies = res.cookies.get_dict()
    print(cookies)
    jar1 = RequestsCookieJar()
    for cookie in cookies:
        jar1.set(cookie['name'], cookie['value'])
        # print(cookie)
    newSession = requests.session()
    newSession.cookies
    res = newSession.get(url=url, headers=headers, cookies=jar1)
    print("内部", res.text)
    print(type(res))
    return res.content
    # try:
    #     jar = getCookies(username, password)
    #     res = requests.get(url=jw_url, cookies=jar)
    #     cookies = requests.cookies
    #     jar1 = RequestsCookieJar()
    #     for cookie in cookies:
    #         jar.set(cookie['name'], cookie['value'])
    #         # print(cookie)
    #     newSession = requests.session()
    #     res = newSession.get(url=url, cookies=jar1)
    #     print("内部", res.text)
    #     print("内部", res.text)
    #     print(type(res))
    #     return res.content
    # except Exception:
    #     print("查询失败，请检查用户名和密码及网络！")
