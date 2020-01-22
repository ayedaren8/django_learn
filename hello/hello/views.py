# -*- coding: utf-8 -*-
from django.http import HttpResponse
from ehall.login import login, jw_login
from django.http import JsonResponse
import json

username = "175043115"
password = "Ygq520123456!"


def netCost(request):
    url = "http://ehall.cidp.edu.cn/jsonp/personalRemind/getViewDataDetail.do?wid=950af967525b4bffb3db654958683e3d&mailAccount=&_=1575341578516"
    r = login(url=url, username=username,  password=password)
    res = {
        "dataFlow": r["imptInfo"]
    }
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")


def course(request):
    url = "http://ehall.cidp.edu.cn/publicapp/sys/pubwdkbapp/api/getMyTimeTableList.do?_=1575360061762"
    res = login(url=url,  username=username,  password=password)
    # res = {
    #     "dataFlow": r["imptInfo"]
    # }
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")


def grade(request):
    url = "https://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx"
    res = jw_login(url=url,  username=username,  password=password)
    # res = {
    #     "dataFlow": r["imptInfo"]
    # }
    return HttpResponse(res, content_type="text/html,charset=utf-8")
