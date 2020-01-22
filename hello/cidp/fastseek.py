import cidp.gologin as gl
import json


def __init__(self, url, username, password):
    self.url = url
    self.username = username
    self.password = password


def getRes(self):
    try:
        self.jar = gl.getCookies(self.username, self.password)
        print(self.jar)
        self.res = gl.doSometing(self.jar, url=self.url)
        self.res = self.res.getRes().text.strip('[]')
        self.res = json.loads(self.res)
        print("内部", self.res)
        return self.res
    except Exception:
        print("查询失败，请检查用户名和密码及网络！")


def getDict(self):
    pass
