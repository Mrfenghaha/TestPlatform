# -*- coding: utf-8 -
from flask import *
from src.main.platform.common.logger import log
from src.main.platform.interface.orthogonal import Orthogonal
from src.main.platform.interface.mockServer import MockServer
from src.main.platform.interface.mockServerConfigs import MockServerConfigs
from src.main.platform.interface.mockServerResponse import MockServerResponse
from src.main.platform.interface.dbOperation import DBOperation
from src.main.platform.interface.dbOperationConfigs import DBOperationConfigs


class Interface:
    def __init__(self, url, request):
        self.url = url
        self.request = request
        self.method = request.method
        self.interface_list = [{"url": "tool/orthogonal", "method": "POST"},
                               {"url": "tool/mock_server/get_mock_list", "method": "GET"},
                               {"url": "tool/mock_server/add_mock", "method": "POST"},
                               {"url": "tool/mock_server/delete_mock", "method": "DELETE"},
                               {"url": "tool/mock_server/update_mock", "method": "PUT"},
                               {"url": "tool/mock_server/get_response_list", "method": "GET"},
                               {"url": "tool/mock_server/add_response", "method": "POST"},
                               {"url": "tool/mock_server/delete_response", "method": "DELETE"},
                               {"url": "tool/mock_server/update_response", "method": "PUT"},
                               {"url": "tool/mock_server/get_configs", "method": "GET"},
                               {"url": "tool/db_operation/get_config_list", "method": "GET"},
                               {"url": "tool/db_operation/add_config", "method": "POST"},
                               {"url": "tool/db_operation/delete_config", "method": "DELETE"},
                               {"url": "tool/db_operation/update_config", "method": "PUT"},
                               {"url": "tool/db_operation/get_operation_list", "method": "GET"},
                               {"url": "tool/db_operation/add_operation", "method": "POST"},
                               {"url": "tool/db_operation/delete_operation", "method": "DELETE"},
                               {"url": "tool/db_operation/update_operation", "method": "PUT"},
                               {"url": "tool/db_operation/execute_operation", "method": "POST"}]

    def judge(self):
        for interface in self.interface_list:
            if self.url == interface['url']:
                if self.method == interface['method']:
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
            if self.url == "tool/orthogonal":
                return Orthogonal().get_pairs(self.request)
            # mock_server服务,,展示mock列表
            if self.url == "tool/mock_server/get_mock_list":
                return MockServer().get_mock_list(self.request)
            # mock_server服务,添加mock
            elif self.url == "tool/mock_server/add_mock":
                return MockServer().add_mock_server(self.request)
            # mock_server服务,删除mock
            elif self.url == "tool/mock_server/delete_mock":
                return MockServer().delete_mock_server(self.request)
            # mock_server服务,修改mock
            elif self.url == "tool/mock_server/update_mock":
                return MockServer().update_mock_server(self.request)
            # mock_server服务,mock的响应,展示配置列表
            elif self.url == "tool/mock_server/get_response_list":
                return MockServerResponse().get_mock_response(self.request)
            # mock_server服务,mock的响应,添加一个响应
            elif self.url == "tool/mock_server/add_response":
                return MockServerResponse().add_mock_response(self.request)
            # mock_server服务,mock的响应,删除一个响应
            elif self.url == "tool/mock_server/delete_response":
                return MockServerResponse().delete_mock_response(self.request)
            # mock_server服务,mock的响应,修改一个响应
            elif self.url == "tool/mock_server/update_response":
                return MockServerResponse().update_mock_response(self.request)
            # mock_server服务,获取配置信息
            elif self.url == "tool/mock_server/get_configs":
                return MockServerConfigs().get_mock_configs(self.request)
            # db_operation服务,获取数据库配置列表
            elif self.url == "tool/db_operation/get_config_list":
                return DBOperationConfigs().get_db_config_list(self.request)
            # db_operation服务,添加数据库配置
            elif self.url == "tool/db_operation/add_config":
                return DBOperationConfigs().add_db_config(self.request)
            # db_operation服务,删除数据库配置
            elif self.url == "tool/db_operation/delete_config":
                return DBOperationConfigs().delete_db_config(self.request)
            # db_operation服务,更新数据库配置
            elif self.url == "tool/db_operation/update_config":
                return DBOperationConfigs().update_db_config(self.request)
            # db_operation服务,获取operations列表
            elif self.url == "tool/db_operation/get_operation_list":
                return DBOperation().get_db_operation_list(self.request)
            # db_operation服务,添加operations
            elif self.url == "tool/db_operation/add_operation":
                return DBOperation().add_db_operation(self.request)
            # db_operation服务,删除operations
            elif self.url == "tool/db_operation/delete_operation":
                return DBOperation().delete_db_operation(self.request)
            # db_operation服务,修改operations
            elif self.url == "tool/db_operation/update_operation":
                return DBOperation().update_db_operation(self.request)
            # db_operation服务,执行operations
            elif self.url == "tool/db_operation/execute_operation":
                return DBOperation().execute_db_operation(self.request)
