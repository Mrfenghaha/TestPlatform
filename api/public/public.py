# -*- coding: utf-8 -
from flask import *
from common.logger import Log


# 接口的log打印设置
def log(*parm):

    if parm[0] == 'request':
        request = parm[1]
        Log().info("[收到请求]  req_url=" + request.url + "  params=" + request.method + "  body=" + str(request.data))
    elif parm[0] == 'response':
        request = parm[1]
        response = parm[2]
        Log().info("[返回结果]  req_url=" + request.url + "  resp_status=" + response.status + "  resp=" + str(response.data))
    else:
        Log().info(parm[0])


def error_response(error_message):
    response = Response(json.dumps({"success": False, "error_message": error_message}), content_type='application/json')
    response.status = "400 Bad Request"
    return response


def right_response(data):
    if data is None:
        response = Response(json.dumps({"success": True}), content_type='application/json')
        return response
    else:
        response = Response(json.dumps({"success": True, "data": data}), content_type='application/json')
        return response
