# -*- coding: utf-8 -
from flask import *


# 接口统一的错误返回信息
def error_response(error_message):
    response = Response(json.dumps({"success": False, "error_message": error_message}), content_type='application/json')
    response.status = "400 Bad Request"
    return response


# 接口统一的返回信息
def right_response(data):
    if data is None:
        response = Response(json.dumps({"success": True}), content_type='application/json')
        return response
    else:
        response = Response(json.dumps({"success": True, "data": data}), content_type='application/json')
        return response
