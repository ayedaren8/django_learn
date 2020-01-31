# -*- coding: utf-8 -*-
from django.http import HttpResponse
from ehall.login import login, jw_login, clear_Data, jw_get, jw_get_photo
from django.views.decorators.csrf import csrf_exempt
import json
import time

cardMoney_URL = "http://ehall.cidp.edu.cn/publicapp/sys/myyktzd/api/getConsumeByRange.do?startY=2019&startM=7&endY=2019&endM=12&isOvered=0&_="
netCost_URL = "http://ehall.cidp.edu.cn/jsonp/personalRemind/getViewDataDetail.do?wid=950af967525b4bffb3db654958683e3d&mailAccount=&_="
course_URL = "http://ehall.cidp.edu.cn/publicapp/sys/pubwdkbapp/api/getMyTimeTableList.do?_="
info_URL = "http://ehall.cidp.edu.cn/jsonp/userDesktopInfo.json?type=&_="
specialApi = ["grade", "getInfo"]


def display_time(fun):
    def deco(*args, **kwargs):
        begin = time.time()
        re = fun(*args, **kwargs)
        end = time.time()
        print(fun.__name__, "函数耗时", (end-begin), "秒")
        return re
    return deco


def doFunction(apiname, username, password):
    re = int(round(time.time() * 1000))
    url = eval(apiname + "_URL")+str(re)
    res = login(url, username, password)
    return res


def grade(username, password):
    res = jw_login(username=username, password=password)
    if type(res) is not int:
        res = clear_Data(res[0], res[1])
        return res
    else:
        return res


def getInfo(username, password):
    res = jw_get(username=username, password=password)
    if type(res) is not int:
        return res
    else:
        return res

@csrf_exempt
def getPhoto(request):
    username = json.loads(request.body)["username"]
    password = json.loads(request.body)["password"]
    res = jw_get_photo(username, password)
    if type(res) is not int:
        return HttpResponse(res, content_type="image/jpeg")
    else:
        return HttpResponse(status=res)

@csrf_exempt
def api(request):
    username = json.loads(request.body)["username"]
    password = json.loads(request.body)["password"]
    apiname = json.loads(request.body)["apiname"]
    if apiname in specialApi:
        res = eval(apiname)(username, password)
    else:
        res = doFunction(apiname, username, password)
    if type(res) is not int:
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(status=res)
