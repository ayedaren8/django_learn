# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import JsonResponse
from ehall.login import login, jw_login, clear_Data
import json
import time


username = "175043115"
password = "Ygq520123456!"


def display_time(fun):
    def deco(*args, **kwargs):
        begin = time.time()
        re = fun(*args, **kwargs)
        end = time.time()
        print(fun.__name__, "函数耗时", (end-begin), "秒")
        return re
    return deco


@display_time
def netCost(request):
    url = "http://ehall.cidp.edu.cn/jsonp/personalRemind/getViewDataDetail.do?wid=950af967525b4bffb3db654958683e3d&mailAccount=&_=1575341578516"
    r = login(url=url, username=username,  password=password)
    return HttpResponse(json.dumps(r, ensure_ascii=False), content_type="application/json,charset=utf-8")


@display_time
def course(request):
    url = "http://ehall.cidp.edu.cn/publicapp/sys/pubwdkbapp/api/getMyTimeTableList.do?_=1575360061762"
    res = login(url=url,  username=username,  password=password)
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")


@display_time
def grade(request):
    xueqi, chengji = jw_login(username=username, password=password)
    res = clear_Data(xueqi, chengji)
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")
