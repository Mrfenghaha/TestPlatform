# -*- coding: utf-8 -
from src.main.mysql.func import *
from src.main.platform.interface.public.public import *


class MockServer:

    def get_mock_list(self, request):
        page_num = request.json.get("page_num")
        num = request.json.get("num")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_mock_list(page_num, num)
        if check_result[0] is True:
            data = Func().get_mock_list(page_num, num)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def add_mock_server(self, request):
        url = request.json.get("url")
        method = request.json.get("method")
        is_available = request.json.get("is_available")
        delay = request.json.get("delay")
        resp_code = request.json.get("resp_code")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().add_mock_server(url, method, is_available, delay, resp_code, remark)
        if check_result[0] is True:
            data = Func().add_mock_server(url, method, is_available, delay, resp_code, remark)
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
        method = request.json.get("method")
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

    def get_mock_list(self, page_num, num):
        start = (page_num - 1) * num  # 按照排序从第n个开始(0-*)
        data = database_func("mock_servers", "get", "specific_num_info", start, num)
        for d in data:  # 移除不需要的key、value
            del d['created_at'], d['updated_at'], d['deleted_at']
        return data

    def add_mock_server(self, url, method, is_available, delay, resp_code, remark):
        data = {"url": url, "method": method, "is_available": is_available, "delay": delay, "resp_code": resp_code,
                "remark": remark}
        db_data = database_func("mock_servers", "insert", data)
        # 移除不需要的key、value
        del db_data['created_at'], db_data['updated_at'], db_data['deleted_at']
        return db_data

    def delete_mock_server(self, id):
        database_func("mock_servers", "delete", id)
        response = Response(json.dumps({'success': True}), content_type='application/json')
        return response

    def update_mock_server(self, id, url, method, is_available, delay, resp_code, remark):
        data = {"url": url, "method": method, "is_available": is_available, "delay": delay, "resp_code": resp_code,
                "remark": remark}
        new_data = database_func("mock_servers", "update", id, data)
        # 移除不需要的key、value
        del new_data['created_at'], new_data['updated_at'], new_data['deleted_at']
        return new_data


class CheckParm(DBQuery):

    def get_mock_list(self, page_num, num):

        if type(page_num) != int or type(num) != int:  # 如果url不为int类型(判断空字符和非空字符时的字符类型,空字符的类型是NoneType)
            return False, "param is error, param not filled or type error"
        elif page_num <= 0:
            return False, "param is error, page_num must > 0"
        elif num < 0:
            return False, "param is error, num must >= 0"
        else:
            return True, None

    def add_mock_server(self, url, method, is_available, delay, resp_code, remark):
        methods_list = self.db_query()[0]
        url_list = self.db_query()[2]
        is_available_list = ["yes", "no"]

        # 必填参数验证(未传类型NoneType)、必填参数传参类型是否正确
        if type(url) != str or type(method) != str or type(is_available) != str or type(delay) != int \
                or type(resp_code) != int or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(url) > 255 or len(method) > 25 or len(is_available) > 25:
            return False, "param is error, param is too long"
        # 具体字段进行具体的判断
        elif url in url_list:
            return False, "param is error, url already exist"
        elif method not in methods_list:
            return False, "param is error, method not exist"
        elif is_available not in is_available_list:
            return False, "param is error, is_available only 'yes' or 'no'"
        elif delay < 0:
            return False, "param is error, delay must >= 0"
        elif resp_code < 0:
            return False, "param is error, resp_code must >= 0"
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
        is_available_list = ["yes", "no"]

        if type(id) != int or type(url) != str or type(method) != str or type(is_available) != str \
                or type(delay) != int or type(resp_code) != int or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(url) > 255 or len(method) > 25 or len(is_available) > 25:
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
                return False, "param is error, is_available only 'yes' or 'no'"
            elif delay < 0:
                return False, "param is error, delay must >= 0"
            elif resp_code < 0:
                return False, "param is error, resp_code must >= 0"
            elif remark == "":
                return False, "param is error, remark cannot be empty"
            else:
                return True, None
