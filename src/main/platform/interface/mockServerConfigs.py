# -*- coding: utf-8 -
from src.main.mysql.func import *
from src.main.platform.interface.public.public import *


class MockServerConfigs:

    def get_mock_configs(self, request):
        data = Func().get_mock_configs()
        return right_response(data)


class DBQuery:

    def db_query(self):
        # 动态数据库查询,所以写在方法中每次调用每次获取
        methods_list = []  # 请求方式列表
        for mt in database_func("mock_configs", "get", "all_value_by_parm", "req_method"):
            methods_list.append(mt.value)

        resp_status_list = []  # 响应状态列表
        for resp_status in database_func("mock_configs", "get", "all_value_by_parm", "resp_status"):
            resp_status_list.append(resp_status.value)

        replace_param_info = []  # 响应替换参数信息(参数名称、备注)
        for info in database_func("mock_configs", "get", "all_value_remark_by_parm", "replace_param"):
            replace_param_info.append({"param": info.value, "remark": info.remark})

        return methods_list, resp_status_list, replace_param_info


class Func(DBQuery):

    def get_mock_configs(self):
        methods_list = self.db_query()[0]
        resp_status_list = self.db_query()[1]
        replace_param_info = self.db_query()[2]
        data = {"method": methods_list, "resp_status": resp_status_list, "replace_param": replace_param_info}
        return data
