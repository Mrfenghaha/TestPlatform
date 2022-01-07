# -*- coding: utf-8 -
import pytest
from src.main.platform.interface.db_operation_configs import *


class TestCheckParmAddDBConfigs:

    def test_check_add_db_configs(self):
        # 合法传参验证
        other = {"name": "login", "ip": "172.16.0.30", "port": 3306, "username": "qy", "password": "xxxx", "remark": "测试传参"}
        data = CheckParm().add_db_configs(other["name"], other["ip"], other["port"], other["username"], other["password"],
                                          other["remark"])
        assert data[0] is True
        assert data[1] is None

    def test_check_add_db_configs_01(self):
        # name不合法传参验证
        name = [None, 1, ("1", "2"), [], {"a": "b"}, "",
                "01234567890123456789012345678901234567890123456789012345678901234"]
        other = {"ip": "172.16.0.30", "port": 3306, "username": "qy", "password": "xxxx", "remark": "测试传参"}
        for n in name:
            data = CheckParm().add_db_configs(n, other["ip"], other["port"], other["username"], other["password"],
                                              other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"
        # name已经存在,验证
        name = "phl_dev"
        if name in DBQuery().db_query()[0]:
            pass
        else:
            Func().add_db_configs(name, other["ip"], other["port"], other["username"], other["password"], other["remark"])
        data = CheckParm().add_db_configs('phl_dev', other["ip"], other["port"], other["username"], other["password"],
                                          other["remark"])
        assert data[0] is False
        assert data[1][0:15] == "param is error,"

    def test_check_add_db_configs_02(self):
        # ip不合法传参验证
        ip = [None, 1, ("1", "2"), [], {"a": "b"}, "",
              "01234567890123456789012345678901234567890123456789012345678901234"]
        other = {"name": "india_dev_db", "port": 3306, "username": "qy", "password": "xxxx", "remark": "测试传参"}
        for i in ip:
            data = CheckParm().add_db_configs(other["name"], i, other["port"], other["username"], other["password"],
                                              other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_add_db_configs_03(self):
        # port不合法传参验证
        port = [None, "aaa", ("1", "2"), [], {"a": "b"}, -1]
        other = {"name": "india_dev_db", "ip": "172.16.0.30", "username": "qy", "password": "xxxx", "remark": "测试传参"}
        for p in port:
            data = CheckParm().add_db_configs(other["name"], other["ip"], p, other["username"], other["password"],
                                              other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_add_db_configs_04(self):
        # username不合法传参验证
        username = [None, 1, ("1", "2"), [], {"a": "b"}, "",
                    "01234567890123456789012345678901234567890123456789012345678901234"]
        other = {"name": "india_dev_db", "ip": "172.16.0.30", "port": 3306, "password": "xxxx", "remark": "测试传参"}
        for u in username:
            data = CheckParm().add_db_configs(other["name"], other["ip"], other["port"], u, other["password"],
                                              other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_add_db_configs_05(self):
        # password不合法传参验证
        password = [None, 1, ("1", "2"), [], {"a": "b"}, "",
                    "01234567890123456789012345678901234567890123456789012345678901234"]
        other = {"name": "india_dev_db", "ip": "172.16.0.30", "port": 3306, "username": "qy", "remark": "测试传参"}
        for pwd in password:
            data = CheckParm().add_db_configs(other["name"], other["ip"], other["port"], other["username"], pwd,
                                              other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_add_db_configs_06(self):
        # remark不合法传参验证
        remark = [None, 1, ("1", "2"), [], {"a": "b"}, ""]
        other = {"name": "india_dev_db", "ip": "172.16.0.30", "port": 3306, "username": "qy", "password": "xxxx"}
        for r in remark:
            data = CheckParm().add_db_configs(other["name"], other["ip"], other["port"], other["username"],
                                              other["password"], r)
            assert data[0] is False
            assert data[1][0:15] == "param is error,"


class TestCheckParmDeleteDBConfigs:
    def test_check_delete_db_configs(self):
        # remark不合法传参验证
        id = 1
        data = CheckParm().delete_db_configs(id)
        assert data[0] is True
        assert data[1] is None

    def test_check_delete_db_configs_01(self):
        # remark不合法传参验证
        id = [None, "aaa", ("1", "2"), [], {"a": "b"}, -1]
        for i in id:
            data = CheckParm().delete_db_configs(i)
            assert data[0] is False
            assert data[1][0:15] == "param is error,"


class TestCheckParmUpdateDBConfigs:

    def test_check_update_db_configs(self):
        # 合法传参验证
        other = {"id": 1, "name": "india_dev_db", "ip": "172.16.0.30", "port": 3306, "username": "qy", "password": "xxxx",
                 "remark": "测试传参"}
        data = CheckParm().update_db_configs(other["id"], other["name"], other["ip"], other["port"], other["username"],
                                             other["password"], other["remark"])
        assert data[0] is True
        assert data[1] is None

    def test_check_update_db_configs_01(self):
        # id不合法传参验证
        id = [None, "aaa", ("1", "2"), [], {"a": "b"}, -1]
        other = {"name": "india_dev_db", "ip": "172.16.0.30", "port": 3306, "username": "qy", "password": "xxxx",
                 "remark": "测试传参"}
        for i in id:
            data = CheckParm().update_db_configs(i, other["name"], other["ip"], other["port"], other["username"],
                                                 other["password"], other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"
        # id不存在,验证
        while True:
            id = 0
            id += id
            if id in DBQuery().db_query()[1]:
                pass
            else:
                break
        data = CheckParm().update_db_configs(id, other["name"], other["ip"], other["port"], other["username"],
                                             other["password"], other["remark"])
        assert data[0] is False
        assert data[1][0:15] == "param is error,"

    def test_check_update_db_configs_02(self):
        # name不合法传参验证
        name = [None, 1, ("1", "2"), [], {"a": "b"}, "",
                "01234567890123456789012345678901234567890123456789012345678901234"]
        other = {"id": 1, "ip": "172.16.0.30", "port": 3306, "username": "qy", "password": "xxxx", "remark": "测试传参"}
        for n in name:
            data = CheckParm().update_db_configs(other["id"], n, other["ip"], other["port"], other["username"],
                                                 other["password"], other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"
        # name已经存在,验证
        name = "phl_dev"
        if name in DBQuery().db_query()[0]:
            pass
        else:
            Func().add_db_configs(name, other["ip"], other["port"], other["username"], other["password"], other["remark"])
        data = CheckParm().add_db_configs('phl_dev', other["ip"], other["port"], other["username"], other["password"],
                                          other["remark"])
        assert data[0] is False
        assert data[1][0:15] == "param is error,"

    def test_check_update_db_configs_03(self):
        # ip不合法传参验证
        ip = [None, 1, ("1", "2"), [], {"a": "b"}, "",
              "01234567890123456789012345678901234567890123456789012345678901234"]
        other = {"id": 1, "name": "india_dev_db", "port": 3306, "username": "qy", "password": "xxxx", "remark": "测试传参"}
        for i in ip:
            data = CheckParm().update_db_configs(other["id"], other["name"], i, other["port"], other["username"],
                                                 other["password"], other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_update_db_configs_04(self):
        # port不合法传参验证
        port = [None, "aaa", ("1", "2"), [], {"a": "b"}, -1]
        other = {"id": 1, "name": "india_dev_db", "ip": "172.16.0.30", "username": "qy", "password": "xxxx",
                 "remark": "测试传参"}
        for p in port:
            data = CheckParm().update_db_configs(other["id"], other["name"], other["ip"], p, other["username"],
                                                 other["password"], other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_update_db_configs_05(self):
        # username不合法传参验证
        username = [None, 1, ("1", "2"), [], {"a": "b"}, "",
                    "01234567890123456789012345678901234567890123456789012345678901234"]
        other = {"id": 1, "name": "india_dev_db", "ip": "172.16.0.30", "port": 3306, "password": "xxxx",
                 "remark": "测试传参"}
        for u in username:
            data = CheckParm().update_db_configs(other["id"], other["name"], other["ip"], other["port"], u,
                                                 other["password"], other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_update_db_configs_06(self):
        # password不合法传参验证
        password = [None, 1, ("1", "2"), [], {"a": "b"}, "",
                    "01234567890123456789012345678901234567890123456789012345678901234"]
        other = {"id": 1, "name": "india_dev_db", "ip": "172.16.0.30", "port": 3306, "username": "qy", "remark": "测试传参"}
        for pwd in password:
            data = CheckParm().update_db_configs(other["id"], other["name"], other["ip"], other["port"],
                                                 other["username"], pwd, other["remark"])
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_update_db_configs_07(self):
        # remark不合法传参验证
        remark = [None, 1, ("1", "2"), [], {"a": "b"}, ""]
        other = {"id": 1, "name": "india_dev_db", "ip": "172.16.0.30", "port": 3306, "username": "qy", "password": "xxxx"}
        for r in remark:
            data = CheckParm().update_db_configs(other["id"], other["name"], other["ip"], other["port"],
                                                 other["username"], other["password"], r)
            assert data[0] is False
            assert data[1][0:15] == "param is error,"


class TestCheckParmGetDBConfigsList:

    def test_check_get_db_configs_list(self):
        # 合法传参验证
        data = CheckParm().get_db_configs_list(1, 10)
        assert data[0] is True
        assert data[1] is None

    def test_check_get_db_configs_list_01(self):
        # page_num不合法传参验证
        page_num = [None, "aaa", ("1", "2"), [], {"a": "b"}, 0]
        for pn in page_num:
            data = CheckParm().get_db_configs_list(pn, 10)
            assert data[0] is False
            assert data[1][0:15] == "param is error,"

    def test_check_get_db_configs_list_02(self):
        # page_num不合法传参验证
        num = [None, "aaa", ("1", "2"), [], {"a": "b"}, -1]
        for n in num:
            data = CheckParm().get_db_configs_list(1, n)
            assert data[0] is False
            assert data[1][0:15] == "param is error,"


class TestDBQuery:

    def test_db_query(self):
        data = DBQuery().db_query()
        assert type(data[0]) == list
        assert type(data[1]) == list


if __name__ == '__main__':
    pytest.main()
