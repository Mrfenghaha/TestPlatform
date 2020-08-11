# -*- coding: utf-8 -
import json
from urllib import parse
from src.main.mysql.func import *
from src.main.platform.interface.public.public import *


class MockServer:

    def get_mock_list(self, request):
        parms = parse.parse_qs(parse.urlparse(request.url).query)
        try:
            page = int(parms["page"][0])
        except:
            page = 1
        try:
            size = int(parms["size"][0])
        except:
            size = 10

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_mock_list(page, size)
        if check_result[0] is True:
            data = Func().get_mock_list(page, size)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def add_mock_server(self, request):
        url = request.json.get("url")
        method = request.json.get("methods")
        is_available = request.json.get("is_available")
        delay = request.json.get("delay")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().add_mock_server(url, method, is_available, delay, remark)
        if check_result[0] is True:
            data = Func().add_mock_server(url, method, is_available, delay, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def delete_mock_server(self, request):
        id = request.json.get("id")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().delete_mock_server(id)
        if check_result[0] is True:
            Func().delete_mock_server(id)
            return right_response(None)
        else:
            return error_response(check_result[1])

    def update_mock_server(self, request):
        id = request.json.get("id")
        url = request.json.get("url")
        method = request.json.get("methods")
        is_available = request.json.get("is_available")
        delay = request.json.get("delay")
        resp_code = request.json.get("resp_code")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().update_mock_server(id, url, method, is_available, delay, resp_code, remark)
        if check_result[0] is True:
            data = Func().update_mock_server(id, url, method, is_available, delay, resp_code, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])


class DBQuery:

    def db_query(self):
        # 动态数据库查询,所以写在方法中每次调用每次获取
        methods_list = []  # 请求方式列表
        for mt in database_func("mock_configs", "get", "all_value_by_parm", "req_method"):
            methods_list.append(mt.value)

        mock_id_list = []  # mock服务id列表
        for mt in database_func("mock_servers", "get", "all_id"):
            mock_id_list.append(mt.id)

        url_list = []  # mock服务url列表
        for mt in database_func("mock_servers", "get", "all_url"):
            url_list.append(mt.url)

        return methods_list, mock_id_list, url_list


class Func(DBQuery):

    def get_mock_list(self, page, size):
        start = (page - 1) * size  # 按照排序从第n个开始(0-*)
        content = database_func("mock_servers", "get", "specific_num_info", start, size)
        for con in content:  # 移除不需要的key、value
            mock_id, resp_code = con['id'], con['resp_code']
            resp_info = database_func("mock_response", "get", "first_by_mockId_code", mock_id, resp_code)
            con['response'] = {"status": resp_info['resp_status'], "headers": json.loads(resp_info['resp_headers']),
                               "body": json.loads(resp_info['resp_body'])}
            del con['created_at'], con['updated_at'], con['deleted_at']
        total = database_func("mock_servers", "get", "all_info_count")  # 获取总条数
        data = {"content": content, "total": total}
        return data

    def add_mock_server(self, url, method, is_available, delay, remark):
        # 添加mock
        data = {"url": url, "method": method, "is_available": is_available, "delay": delay, "resp_code": 0,
                "remark": remark}
        db_data = database_func("mock_servers", "insert", data)
        del db_data['created_at'], db_data['updated_at'], db_data['deleted_at']  # 移除不需要的key、value
        # 添加默认的response
        resp_data = {"mock_id": db_data['id'], "resp_code": 0, "resp_status": '200 OK',
                     "resp_headers": '{"content-type": "application/json"}',
                     "resp_body": '{"success": true}', "remark": '默认成功返回200'}
        database_func("mock_response", "insert", resp_data)
        return db_data

    def delete_mock_server(self, id):
        database_func("mock_servers", "delete", id)

    def update_mock_server(self, id, url, method, is_available, delay, resp_code, remark):
        data = {"url": url, "method": method, "is_available": is_available, "delay": delay, "resp_code": resp_code,
                "remark": remark}
        new_data = database_func("mock_servers", "update", id, data)
        # 移除不需要的key、value
        del new_data['created_at'], new_data['updated_at'], new_data['deleted_at']
        return new_data


class CheckParm(DBQuery):

    def get_mock_list(self, page, size):
        if type(page) != int or type(size) != int:
            return False, "param is error, param not filled or type error"
        elif page <= 0 or size <= 0:
            return False, "param is error, page and size must > 0"
        else:
            return True, None

    def add_mock_server(self, url, method, is_available, delay, remark):
        methods_list = self.db_query()[0]
        url_list = self.db_query()[2]
        is_available_list = [1, 0]

        # 必填参数验证(未传类型NoneType)、必填参数传参类型是否正确
        if type(url) != str or type(method) != str or type(is_available) != int or type(delay) != int or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(url) > 255 or len(method) > 25:
            return False, "param is error, param is too long"
        # 具体字段进行具体的判断
        elif url in url_list:
            return False, "param is error, url already exist"
        elif method not in methods_list:
            return False, "param is error, method not exist"
        elif is_available not in is_available_list:
            return False, "param is error, is_available only 1 or 0"
        elif delay < 0:
            return False, "param is error, delay must >= 0"
        elif remark == "":
            return False, "param is error, remark cannot be empty"
        else:
            return True, None

    def delete_mock_server(self, id):
        mock_id_list = self.db_query()[1]

        if type(id) != int:
            return False, "param is error, param not filled or type error"
        elif id < 0:
            return False, "param is error, id must >= 0"
        elif id not in mock_id_list:
            return False, "param is error, id not exist"
        else:
            return True, None

    def update_mock_server(self, id, url, method, is_available, delay, resp_code, remark):
        methods_list = self.db_query()[0]
        mock_id_list = self.db_query()[1]
        url_list = self.db_query()[2]
        is_available_list = [1, 0]

        if type(id) != int or type(url) != str or type(method) != str or type(is_available) != int \
                or type(delay) != int or type(resp_code) != int or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(url) > 255 or len(method) > 25:
            return False, "param is error, param is too long"
        elif id < 0:
            return False, "param is error, id must >= 0"
        elif id not in mock_id_list:
            return False, "param is error, id not exist"
        else:
            url_list.remove(database_func("mock_servers", "get", 'first_by_id', id)['url'])  # 修改需要移除当前url判断
            if url in url_list:
                return False, "param is error, url already exist"
            elif method not in methods_list:
                return False, "param is error, method not exist"
            elif is_available not in is_available_list:
                return False, "param is error, is_available only 1 or 0"
            elif delay < 0:
                return False, "param is error, delay must >= 0"
            elif resp_code < 0:
                return False, "param is error, resp_code must >= 0"
            elif remark == "":
                return False, "param is error, remark cannot be empty"
            else:
                return True, None
