from ehall.Spider import Spider
import json


class SpiderJw(Spider):
    "教务爬虫，用于处理教务管理系统的成绩部分"

    def __init__(self, username, password, url):
        self.url = url
        super().__init__(url=self.url, username=username, password=password)
        self.xueqi = ''
        self.chengji = ''

    def CHECK(fun):
        def inner(self, *args, **kwargs):
            if len(self.errorList) == 0:
                fun(self, *args, **kwargs)
            else:
                print(fun.__name__+"未运行，因为" + str(self.errorList))
        return inner

    @CHECK
    def openRequest(self):
        print("SpiderJw爬虫")
        url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3a%2f%2fjw.cidp.edu.cn%2fLoginHandler.ashx"
        try:
            driver = self.driver
            driver.get(url=url)
            driver.find_element_by_name('username').send_keys(self.username)
            driver.find_element_by_id('password').send_keys(self.password)
            driver.find_element_by_tag_name('button').click()
            self.driver = driver
        except Exception:
            self.errorList.append("findError")
            driver.quit()

    @CHECK
    def grep(self):
        try:
            driver = self.driver
            driver.get(
                url="https://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx")
            print(driver.title)
            if driver.title == "无权限，请重试":
                self.errorList.append("pwdError")
                driver.quit()
            else:
                xueqi = driver.find_element_by_xpath(
                    "//input[@id='hfSemesterFramework']")
                chengji = driver.find_element_by_xpath(
                    "//input[@id='hfAverageMarkFromClass']")
                xueqi = xueqi.get_attribute("value")
                chengji = chengji.get_attribute("value")
                driver.quit()
                self.xueqi = json.loads(xueqi)
                self.chengji = json.loads(chengji)
        except Exception as e:
            print(e)
            self.errorList.append("findErrors")

    @CHECK
    def clear_Data(self):
        for year in self.xueqi:
            for i in year["List"]:
                gradeList = []
                for n in self.chengji:
                    if int(i["SemesterId"]) == int(n["SemesterID"]):
                        gradeList.append(n)
                i.update({"gradeList": gradeList})
        self.res = self.xueqi
        print(self.xueqi)

    @CHECK
    def sendBack(self):
        self.clear_Data()

    def run(self):
        if self.isNeedCap is False:
            self.openBrowser()
            self.openRequest()
            self.grep()
            self.check()
            self.quit()
            return self.errorList, self.res
        else:
            for i in self.errorList:
                print(i)
            return self.errorList
