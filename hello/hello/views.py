# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import JsonResponse
from ehall.login import login, jw_login, clear_Data
from django.views.decorators.csrf import csrf_exempt
import json
import time

cardMoney_URl = "http://ehall.cidp.edu.cn/publicapp/sys/myyktzd/api/getConsumeByRange.do?startY=2019&startM=7&endY=2019&endM=12&isOvered=0&_=1575360061774"
netCost_URL = "http://ehall.cidp.edu.cn/jsonp/personalRemind/getViewDataDetail.do?wid=950af967525b4bffb3db654958683e3d&mailAccount=&_=1575341578516"
course_URL = "http://ehall.cidp.edu.cn/publicapp/sys/pubwdkbapp/api/getMyTimeTableList.do?_=1575360061762"
info_URL = "http://ehall.cidp.edu.cn/jsonp/userDesktopInfo.json?type=&_=1575365028115"


def display_time(fun):
    def deco(*args, **kwargs):
        begin = time.time()
        re = fun(*args, **kwargs)
        end = time.time()
        print(fun.__name__, "函数耗时", (end-begin), "秒")
        return re
    return deco


def doFunction(apiname,username,password):
    url = eval(apiname + "_URL")
    res=login(url,username,password)
    return res



def cardMoney(username, password):
    url = CARD_URL
    res = login(url=url, username=username, password=password)
    return res



def netCost(username, password):
    url = netCost_URL
    res = login(url=url, username=username,  password=password)
    return res


def course(username, password):
    url = course_URL
    res = login(url=url, username=username, password=password)
    return res



def grade(username, password):
    res = jw_login(username=username, password=password)
    if type(res) is not int:
        res = clear_Data(res[0], res[1])
        return res
    else:
        return res


def info(username, password):
    url = info_URL
    res = login(url=url, username=username, password=password)
    return res


@csrf_exempt
def api(request):
    username = json.loads(request.body)["username"]
    password = json.loads(request.body)["password"]
    apiname = json.loads(request.body)["apiname"]
    res = eval(apiname)(username, password)
    if type(res) is not int:
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(status=res)
