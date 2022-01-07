# -*- coding: utf-8 -
from urllib import parse
from src.main.mysql.func import *
from src.main.platform.interface.public.public import *


class MockServerResponse:

    def get_mock_response(self, request):
        parm = parse.parse_qs(parse.urlparse(request.url).query)
        parms = {k: v[0] for k, v in parm.items()}
        mock_id = parms.get("mock_id")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_mock_response(mock_id)
        if check_result[0] is True:
            data = Func().get_mock_response(int(mock_id))
            return right_response(data)
        else:
            return error_response(check_result[1])

    def add_mock_response(self, request):
        mock_id = request.json.get("mock_id")
        name = request.json.get("name")
        status = request.json.get("status")
        headers = request.json.get("headers")
        body = request.json.get("body")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().add_mock_response(mock_id, name, status, headers, body, remark)
        if check_result[0] is True:
            data = Func().add_mock_response(mock_id, name, status, headers, body, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def delete_mock_response(self, request):
        id = request.json.get("id")
        mock_id = request.json.get("mock_id")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().delete_mock_response(mock_id, id)
        if check_result[0] is True:
            Func().delete_mock_response(id)
            return right_response(None)
        else:
            return error_response(check_result[1])

    def update_mock_response(self, request):
        id = request.json.get("id")
        mock_id = request.json.get("mock_id")
        name = request.json.get("name")
        status = request.json.get("status")
        headers = request.json.get("headers")
        body = request.json.get("body")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().update_mock_response(id, mock_id, name, status, headers, body, remark)
        if check_result[0] is True:
            data = Func().update_mock_response(id, mock_id, name, status, headers, body, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])


class DBQuery:

    def db_query(self):
        # 动态数据库查询,所以写在方法中每次调用每次获取
        status_list = [status.value for status in database_func("mock_configs", "get", "all_value_by_parm", "resp_status")]  # 响应状态列表
        mock_id_list = [mt.id for mt in database_func("mock_servers", "get", "all_id")]  # mock服务id列表
        id_list = [mt.id for mt in database_func("mock_response", "get", "all_id")]  # 响应id列表
        return status_list, mock_id_list, id_list


class Func(DBQuery):

    def get_mock_response(self, mock_id):
        data = database_func("mock_response", "get", "all_by_mockId", mock_id)
        for d in data:  # 移除不需要的key、value
            del d['created_at'], d['updated_at'], d['deleted_at']
        return data

    def add_mock_response(self, mock_id, name, status, headers, body, remark):
        data = {"mock_id": mock_id, "name": name, "status": status, "headers": headers, "body": body, "remark": remark,
                "is_default": 0}
        db_data = database_func("mock_response", "insert", data)
        del db_data['created_at'], db_data['updated_at'], db_data['deleted_at']
        return db_data

    def delete_mock_response(self, id):
        database_func("mock_response", "delete", "first_by_id", id)

    def update_mock_response(self, id, mock_id, name, status, headers, body, remark):
        data = {"mock_id": mock_id, "name": name, "status": status, "headers": headers, "body": body, "remark": remark}
        new_data = database_func("mock_response", "update", "first_by_id", id, data)
        del new_data['created_at'], new_data['updated_at'], new_data['deleted_at']
        return new_data


class CheckParm(DBQuery):

    def get_mock_response(self, mock_id):
        mock_id_list = self.db_query()[1]

        try:
            mock_id = int(mock_id)
        except:
            return False, "param is error, param not filled or type error"
        if mock_id not in mock_id_list:
            return False, "param is error, mock_id not exist"
        else:
            return True, None

    def add_mock_response(self, mock_id, name, status, headers, body, remark):
        status_list = self.db_query()[0]
        mock_id_list = self.db_query()[1]

        if type(mock_id) != int or type(name) != str or type(status) != str or type(headers) != str or \
                type(body) != str or type(remark) != str:
            return False, "param  is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(name) > 64 or len(status) > 64:
            return False, "param is error, param is too long"
        elif mock_id not in mock_id_list:
            return False, "param is error, mock_id not exist"
        elif status not in status_list:
            return False, "param is error, status not exist"
        elif name == "" or remark == "":
            return False, "param is error, param cannot be empty"
        else:  # 判断需要同接口其他参数(该参数也需要校验的),先满足前置条件的校验,在校验当前参数
            name_list = [mt.name for mt in database_func("mock_response", "get", "all_name_by_mockId", mock_id)]
            if name in name_list:
                return False, "param is error, name already exist"
            else:
                return True, None

    def delete_mock_response(self, mock_id, id):
        mock_id_list = self.db_query()[1]
        id_list = self.db_query()[2]

        if type(mock_id) != int or type(id) != int:
            return False, "param is error, param not filled or type error"
        elif id not in id_list:
            return False, "param is error, id not exist"
        elif mock_id not in mock_id_list:
            return False, "param is error, mock_id not exist"
        else:
            id_list_by_mock_id = [mt.id for mt in database_func("mock_response", "get", "all_id_by_mockId", mock_id)]
            if id not in id_list_by_mock_id:
                return False, "delete failed, id and mock_id don't match"
            else:
                name_list = [mt.name for mt in database_func("mock_response", "get", "all_name_by_mockId", mock_id)]
                if len(name_list) == 1:
                    return False, "delete failed, last response cannot be deleted"
                else:
                    return True, None

    def update_mock_response(self, id, mock_id, name, status, headers, body, remark):
        status_list = self.db_query()[0]
        mock_id_list = self.db_query()[1]
        id_list = self.db_query()[2]

        if type(id) != int or type(mock_id) != int or type(name) != str or type(status) != str \
                or type(headers) != str or type(body) != str or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(name) > 64 or len(status) > 64:
            return False, "param is error, param is too long"
        elif id not in id_list:
            return False, "param is error, id not exist"
        elif mock_id not in mock_id_list:
            return False, "param is error, mock_id not exist"
        elif status not in status_list:
            return False, "param is error, status not exist"
        elif name == "" or remark == "":
            return False, "param is error, param cannot be empty"
        else:  # 判断需要同接口其他参数(该参数也需要校验的),先满足前置条件的校验,在校验当前参数
            name_list = [mt.name for mt in database_func("mock_response", "get", "all_name_by_mockId", mock_id)]
            # 更新时name_list需要去除当前name
            name_list.remove(database_func("mock_response", "get", 'first_by_id', id)['name'])
            if name in name_list:
                return False, "param is error, name already exist"
            else:
                id_list_by_mock_id = [mt.id for mt in database_func("mock_response", "get", "all_id_by_mockId", mock_id)]
                if id not in id_list_by_mock_id:
                    return False, "param is error, id and mock_id don't match"
                return True, None
