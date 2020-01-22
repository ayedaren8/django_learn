from selenium import webdriver
import requests


def getCookies(username, password):
    """
       NOTE：
       使用selenium加载Phantoms浏览器驱动
        \\查找表单username和password
        \\获得cooikes 此时获得的是list对象 无法被request使用 需要清洗
        \\关闭驱动 否则多次调试 可能出现句柄错误6 因为上次调用进程未关闭

       RequestsCookieJar()
       \\发送数据的时候向服务器传递cookie，需要实例化一个RequestsCookieJar。
       \\从selenium的返回值cookies获得相应的name和value
       \\用jar这个实例的set方法注入值
    """

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        'Content-Type': 'application/json;charset=UTF-8'}
    url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3A%2F%2Fehall.cidp.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cidp.edu.cn%2Fnew%2Findex.html"
    try:
        driver = webdriver.PhantomJS(executable_path=r'./Phantoms/bin/phantomjs.exe')
        driver.get(url=url, header=header)
        driver.find_element_by_name('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_tag_name('button').click()
        cookies = driver.get_cookies()
        driver.quit()
    except Exception:
        print("模拟登陆出错")
    jar = requests.cookies.RequestsCookieJar()
    for cookie in cookies:
        jar.set(cookie['name'], cookie['value'])
        print(cookie)
    return jar


def doSometing(jar, url):
    """
       NOTE：
       request请求打印显示的返回值是json对象
    """
    res = requests.get(url=url, cookies=jar)
    return res
