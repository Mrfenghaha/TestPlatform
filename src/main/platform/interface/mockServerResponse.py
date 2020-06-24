# -*- coding: utf-8 -
from src.main.mysql.func import *
from src.main.platform.interface.public.public import *


class MockServerResponse:

    def get_mock_response(self, request):
        mock_id = request.json.get("mock_id")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_mock_response(mock_id)
        if check_result[0] is True:
            data = Func().get_mock_response(mock_id)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def add_mock_response(self, request):
        mock_id = request.json.get("mock_id")
        resp_code = request.json.get("resp_code")
        resp_status = request.json.get("resp_status")
        resp_headers = request.json.get("resp_headers")
        resp_body = request.json.get("resp_body")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().add_mock_response(mock_id, resp_code, resp_status, resp_headers, resp_body, remark)
        if check_result[0] is True:
            data = Func().add_mock_response(mock_id, resp_code, resp_status, resp_headers, resp_body, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def delete_mock_response(self, request):
        id = request.json.get("id")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().delete_mock_response(id)
        if check_result[0] is True:
            Func().delete_mock_response(id)
            return right_response(None)
        else:
            return error_response(check_result[1])

    def update_mock_response(self, request):
        id = request.json.get("id")
        mock_id = request.json.get("mock_id")
        resp_code = request.json.get("resp_code")
        resp_status = request.json.get("resp_status")
        resp_headers = request.json.get("resp_headers")
        resp_body = request.json.get("resp_body")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().update_mock_response(id, mock_id, resp_code, resp_status, resp_headers, resp_body,
                                                        remark)
        if check_result[0] is True:
            data = Func().update_mock_response(id, mock_id, resp_code, resp_status, resp_headers, resp_body, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])


class DBQuery:

    def db_query(self):
        # 动态数据库查询,所以写在方法中每次调用每次获取
        resp_status_list = []  # 响应状态列表
        for resp_status in database_func("mock_configs", "get", "all_value_by_parm", "resp_status"):
            resp_status_list.append(resp_status.value)

        mock_id_list = []  # mock服务id列表
        for mt in database_func("mock_servers", "get", "all_id"):
            mock_id_list.append(mt.id)

        resp_id_list = []  # 响应id列表
        for mt in database_func("mock_response", "get", "all_id"):
            resp_id_list.append(mt.id)

        return resp_status_list, mock_id_list, resp_id_list


class Func(DBQuery):

    def get_mock_response(self, mock_id):
        data = database_func("mock_response", "get", "all_by_mockId", mock_id)
        for d in data:  # 移除不需要的key、value
            del d['created_at'], d['updated_at'], d['deleted_at']
        return data

    def add_mock_response(self, mock_id, resp_code, resp_status, resp_headers, resp_body, remark):
        data = {"mock_id": mock_id, "resp_code": resp_code, "resp_status": resp_status,
                "resp_headers": resp_headers, "resp_body": resp_body, "remark": remark}
        db_data = database_func("mock_response", "insert", data)
        del db_data['created_at'], db_data['updated_at'], db_data['deleted_at']
        return db_data

    def delete_mock_response(self, id):
        database_func("mock_response", "delete", id)

    def update_mock_response(self, id, mock_id, resp_code, resp_status, resp_headers, resp_body, remark):
        data = {"mock_id": mock_id, "resp_code": resp_code, "resp_status": resp_status,
                "resp_headers": resp_headers, "resp_body": resp_body, "remark": remark}
        new_data = database_func("mock_response", "update", id, data)
        del new_data['created_at'], new_data['updated_at'], new_data['deleted_at']
        return new_data


class CheckParm(DBQuery):

    def get_mock_response(self, mock_id):
        mock_id_list = self.db_query()[1]

        if type(mock_id) != int:
            return False, "param is error, param not filled or type error"
        elif mock_id not in mock_id_list:
            return False, "param is error, mock_id not exist"
        else:
            return True, None

    def add_mock_response(self, mock_id, resp_code, resp_status, resp_headers, resp_body, remark):
        resp_status_list = self.db_query()[0]
        mock_id_list = self.db_query()[1]

        if type(mock_id) != int or type(resp_code) != int or type(resp_status) != str or type(resp_headers) != str \
                or type(resp_body) != str or type(remark) != str:
            return False, "param  is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(resp_status) > 255:
            return False, "param is error, param is too long"
        elif mock_id not in mock_id_list:
            return False, "param is error, mock_id not exist"
        elif resp_status not in resp_status_list:
            return False, "param is error, resp_status not exist"
        elif remark == "":
            return False, "param is error, remark cannot be empty"
        else:  # 判断需要同接口其他参数(该参数也需要校验的),先满足前置条件的校验,在校验当前参数
            resp_code_list = []
            for mt in database_func("mock_response", "get", "all_respCode_by_mockId", mock_id):
                resp_code_list.append(mt.resp_code)
            if resp_code in resp_code_list:
                return False, "param is error, resp_code already exist"
            else:
                return True, None

    def delete_mock_response(self, id):
        resp_id_list = self.db_query()[2]

        if type(id) != int:
            return False, "param is error, param not filled or type error"
        elif id < 0:
            return False, "param is error, id must >= 0"
        elif id not in resp_id_list:
            return False, "param is error, id not exist"
        else:
            return True, None

    def update_mock_response(self, id, mock_id, resp_code, resp_status, resp_headers, resp_body, remark):
        resp_status_list = self.db_query()[0]
        mock_id_list = self.db_query()[1]
        resp_id_list = self.db_query()[2]

        if type(id) != int or type(mock_id) != int or type(resp_code) != int or type(resp_status) != str \
                or type(resp_headers) != str or type(resp_body) != str or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(resp_status) > 255:
            return False, "param is error, param is too long"
        elif id not in resp_id_list:
            return False, "param is error, id not exist"
        elif mock_id not in mock_id_list:
            return False, "param is error, mock_id not exist"
        elif resp_status not in resp_status_list:
            return False, "param is error, resp_status not exist"
        elif remark == "":
            return False, "param is error, remark cannot be empty"
        else:  # 判断需要同接口其他参数(该参数也需要校验的),先满足前置条件的校验,在校验当前参数
            response_code_list = []
            for mt in database_func("mock_response", "get", "all_respCode_by_mockId", mock_id):
                response_code_list.append(mt.resp_code)
            # 更新时resp_code_list需要去除当前resp_code
            response_code_list.remove(database_func("mock_response", "get", 'first_by_id', id)['resp_code'])

            if resp_code in response_code_list:
                return False, "param is error, resp_code already exist"
            else:
                return True, None
