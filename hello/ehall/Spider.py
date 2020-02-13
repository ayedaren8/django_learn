import requests
from selenium import webdriver
import time
from requests.cookies import RequestsCookieJar


class Spider(object):
    "根爬虫，用于处理ehall大厅的部分请求"
    browser_path = "Phantoms/bin/phantomjs.exe"

    def __init__(self, username, password, url):
        self.open_url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3A%2F%2Fehall.cidp.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cidp.edu.cn%2Fnew%2Findex.html"
        self.url = url
        self.jar = None
        self.driver = None
        self.res = None
        self.errorList = []
        self.username = username
        self.password = password
        self.isNeedCap = None
        self.needCaptcha()

    def needCaptcha(self):
        ts = int(round(time.time() * 1000))
        url = "http://authserver.cidp.edu.cn/authserver/needCaptcha.html?username={username}&pwdEncrypt2=pwdEncryptSalt&_={ts}".format(
            username=self.username, ts=ts)
        res = requests.post(url)
        if res.text == "false":
            self.isNeedCap = False
        else:
            self.isNeedCap = True
            self.errorList.append("capError")

    def openBrowser(self):
        try:
            driver = webdriver.PhantomJS(executable_path=Spider.browser_path)
            self.driver = driver
            return driver
        except Exception as e:
            print(e)
            self.errorList.append("driverError")

    def openRequest(self):
        try:
            driver = self.driver
            driver.get(url=self.open_url)
            driver.find_element_by_name('username').send_keys(self.username)
            driver.find_element_by_id('password').send_keys(self.password)
            driver.find_element_by_tag_name('button').click()
            cookies = driver.get_cookies()
            jar = RequestsCookieJar()
            for cookie in cookies:
                jar.set(cookie['name'], cookie['value'])
            self.jar = jar
            # print("字典",self.jar)
        except Exception as e:
            print(e)
            self.errorList.append("findError")
        finally:
            driver.quit()

    def grep(self):
        res = requests.get(url=self.url, cookies=self.jar)
        if res.url == self.url:
            self.res = res
        else:
            self.errorList.append("pwdError")

    def check(self):
        if len(self.errorList) != 0:
            for i in self.errorList:
                print(i)
        else:
            self.sendBack()

    def sendBack(self):
        # print(self.res.text)
        self.res = self.res.text

    def quit(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(e)

    def run(self):

        if self.isNeedCap is False:
            self.openBrowser()
            self.openRequest()
            self.grep()
            self.check()
            return self.errorList, self.res
        else:
            for i in self.errorList:
                print(i)
            return self.errorList


