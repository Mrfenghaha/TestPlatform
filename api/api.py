# -*- coding: utf-8 -
from api.public.public import *
from api.all_pairs.pairs import *
from api.mock_server.mock import *
from api.mock_server.response import *
from api.mock_server.configs import *
from api.db_operation.configs import *
from api.db_operation.operations import *


class API:
    def __init__(self, url, request):
        self.url = url
        self.request = request
        self.method = request.method
        self.api_list = [{"url": 'all_pairs/pairs/get_pairs', "method": "POST"},
                         {"url": 'mock_server/mock/show_lists', "method": "POST"},
                         {"url": 'mock_server/mock/add', "method": "POST"},
                         {"url": 'mock_server/mock/delete', "method": "POST"},
                         {"url": 'mock_server/mock/update', "method": "POST"},
                         {"url": 'mock_server/response/show_lists', "method": "POST"},
                         {"url": 'mock_server/response/add', "method": "POST"},
                         {"url": 'mock_server/response/delete', "method": "POST"},
                         {"url": 'mock_server/response/update', "method": "POST"},
                         {"url": 'mock_server/configs/info', "method": "GET"},
                         {"url": 'db_operation/configs/show_lists', "method": "POST"},
                         {"url": 'db_operation/configs/add', "method": "POST"},
                         {"url": 'db_operation/configs/delete', "method": "POST"},
                         {"url": 'db_operation/configs/update', "method": "POST"},
                         {"url": 'db_operation/operations/show_lists', "method": "POST"},
                         {"url": 'db_operation/operations/add', "method": "POST"},
                         {"url": 'db_operation/operations/delete', "method": "POST"},
                         {"url": 'db_operation/operations/update', "method": "POST"},
                         {"url": 'db_operation/operations/execute', "method": "POST"}]

    def judge(self):
        for api in self.api_list:
            if self.url == api['url']:
                if self.method == api['method']:
                    return True
                else:
                    log('请求方式错误,响应405')
                    abort(405)
            else:
                pass
        log('请求url不存在,响应404')
        abort(404)

    def api(self):
        if self.judge() is True:
            # all_pairs服务,获取正交组合
            if self.url == 'all_pairs/pairs/get_pairs':
                return AllPairs().get_pairs(self.request)
            # mock_server服务,,展示mock列表
            if self.url == 'mock_server/mock/show_lists':
                return MockServersMock().get_mock_list(self.request)
            # mock_server服务,添加mock
            elif self.url == 'mock_server/mock/add':
                return MockServersMock().add_mock_server(self.request)
            # mock_server服务,删除mock
            elif self.url == 'mock_server/mock/delete':
                return MockServersMock().delete_mock_server(self.request)
            # mock_server服务,修改mock
            elif self.url == 'mock_server/mock/update':
                return MockServersMock().update_mock_server(self.request)
            # mock_server服务,mock的响应,展示配置列表
            elif self.url == 'mock_server/response/show_lists':
                return MockServersResponse().get_mock_response(self.request)
            # mock_server服务,mock的响应,添加一个响应
            elif self.url == 'mock_server/response/add':
                return MockServersResponse().add_mock_response(self.request)
            # mock_server服务,mock的响应,删除一个响应
            elif self.url == 'mock_server/response/delete':
                return MockServersResponse().delete_mock_response(self.request)
            # mock_server服务,mock的响应,修改一个响应
            elif self.url == 'mock_server/response/update':
                return MockServersResponse().update_mock_response(self.request)
            # mock_server服务,获取配置信息
            elif self.url == 'mock_server/configs/info':
                return MockServersConfigs().get_mock_configs(self.request)
            # db_operation服务,获取数据库配置列表
            elif self.url == 'db_operation/configs/show_lists':
                return DBOperationConfigs().get_db_configs_list(self.request)
            # db_operation服务,添加数据库配置
            elif self.url == 'db_operation/configs/add':
                return DBOperationConfigs().add_db_configs(self.request)
            # db_operation服务,删除数据库配置
            elif self.url == 'db_operation/configs/delete':
                return DBOperationConfigs().delete_db_configs(self.request)
            # db_operation服务,更新数据库配置
            elif self.url == 'db_operation/configs/update':
                return DBOperationConfigs().update_db_configs(self.request)
            # db_operation服务,获取operations列表
            elif self.url == 'db_operation/operations/show_lists':
                return DBOperationOperation().get_db_operation_list(self.request)
            # db_operation服务,添加operations
            elif self.url == 'db_operation/operations/add':
                return DBOperationOperation().add_db_operation(self.request)
            # db_operation服务,删除operations
            elif self.url == 'db_operation/operations/delete':
                return DBOperationOperation().delete_db_operation(self.request)
            # db_operation服务,修改operations
            elif self.url == 'db_operation/operations/update':
                return DBOperationOperation().update_db_operation(self.request)
            # db_operation服务,执行operations
            elif self.url == 'db_operation/operations/execute':
                return DBOperationOperation().execute_db_operation(self.request)
