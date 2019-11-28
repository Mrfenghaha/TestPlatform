# -*- coding: utf-8 -
from api.public.public import *
from db.func import *
from common.ase import *
from common.config.readConfig import *


class DBOperationConfigs:

    def get_db_configs_list(self, request):
        page_num = request.json.get("page_num")
        num = request.json.get("num")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_db_configs_list(page_num, num)
        if check_result[0] is True:
            data = Func().get_db_configs_list(page_num, num)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def add_db_configs(self, request):
        name = request.json.get("name")
        ip = request.json.get("ip")
        port = request.json.get("port")
        username = request.json.get("username")
        password = request.json.get("password")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().add_db_configs(name, ip, port, username, password, remark)
        if check_result[0] is True:
            data = Func().add_db_configs(name, ip, port, username, password, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def delete_db_configs(self, request):
        id = request.json.get("id")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().delete_db_configs(id)
        if check_result[0] is True:
            Func().delete_db_configs(id)
            return right_response(None)
        else:
            return error_response(check_result[1])

    def update_db_configs(self, request):
        id = request.json.get("id")
        name = request.json.get("name")
        ip = request.json.get("ip")
        port = request.json.get("port")
        username = request.json.get("username")
        password = request.json.get("password")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().update_db_configs(id, name, ip, port, username, password, remark)
        if check_result[0] is True:
            data = Func().update_db_configs(id, name, ip, port, username, password, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])


class DBQuery:

    def db_query(self):
        # 动态数据库查询,所以写在方法中每次调用每次获取
        db_configs_name_list = []  # 数据库配置名称列表
        for db in database_func("database_configs", "get", "all_name"):
            db_configs_name_list.append(db.name)

        db_configs_id_list = []  # 数据库配置id列表
        for db in database_func("database_configs", "get", "all_id"):
            db_configs_id_list.append(db.id)

        return db_configs_name_list, db_configs_id_list


class Func(DBQuery):

    def get_db_configs_list(self, page_num, num):
        start = (page_num - 1) * num  # 按照排序从第n个开始(0-*)
        data = database_func("database_configs", "get", "specific_num_info", start, num)
        for d in data:  # 返回数据较少,通过赋值的方式进行
            del d['created_at'], d['updated_at'], d['deleted_at']
        return data

    def add_db_configs(self, name, ip, port, username, password, remark):
        pc = PrpCrypt(encryption_key)
        new_username = pc.encrypt(username)
        new_password = pc.encrypt(password)
        data = {"name": name, "ip": ip, "port": port, "username": new_username, "password": new_password,
                "remark": remark}
        db_data = database_func("database_configs", "insert", data)
        del db_data['created_at'], db_data['updated_at'], db_data['deleted_at'], db_data['username'], db_data['password']
        return db_data

    def delete_db_configs(self, id):
        database_func("database_configs", "delete", id)

    def update_db_configs(self, id, name, ip, port, username, password, remark):
        pc = PrpCrypt(encryption_key)
        new_username = pc.encrypt(username)
        new_password = pc.encrypt(password)
        data = {"id": id, "name": name, "ip": ip, "port": port, "username": new_username, "password": new_password,
                "remark": remark}
        new_data = database_func("database_configs", "update", id, data)
        del new_data['created_at'], new_data['updated_at'], new_data['deleted_at'], new_data['username'], new_data['password']
        return new_data


class CheckParm(DBQuery):

    def get_db_configs_list(self, page_num, num):
        if type(page_num) != int or type(num) != int:
            return False, "param is error, param not filled or type error"
        elif page_num <= 0:
            return False, "param is error, page_num must > 0"
        elif num < 0:
            return False, "param is error, num must >= 0"
        else:
            return True, None

    def add_db_configs(self, name, ip, port, username, password, remark):
        db_configs_name_list = self.db_query()[0]

        if type(name) != str or type(ip) != str or type(port) != int or type(username) != str or type(password) != str \
                or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(name) > 64 or len(ip) > 64 or len(username) > 64 or len(password) > 64:
            return False, "param is error, param is too long"
        elif name == "" or ip == "" or username == "" or password == "" or remark == "":
            return False, "param is error, param cannot be empty"
        elif name in db_configs_name_list:
            return False, "param is error, name already exist"
        elif port <= 0:
            return False, "param is error, port must >0"
        else:
            return True, None

    def delete_db_configs(self, id):
        db_configs_id_list = self.db_query()[1]

        if type(id) != int:
            return False, "param is error, param not filled or type error"
        elif id < 0:
            return False, "param is error, id must >= 0"
        elif id not in db_configs_id_list:
            return False, "param is error, id not exist"
        else:
            return True, None

    def update_db_configs(self, id, name, ip, port, username, password, remark):
        db_configs_name_list = self.db_query()[0]
        db_configs_id_list = self.db_query()[1]

        if type(id) != int or type(name) != str or type(ip) != str or type(port) != int or type(username) != str \
                or type(password) != str or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(name) > 64 or len(ip) > 64 or len(username) > 64 or len(password) > 64:
            return False, "param is error, param is too long"
        elif name == "" or ip == "" or username == "" or password == "" or remark == "":
            return False, "param is error, param cannot be empty"
        elif id not in db_configs_id_list:
            return False, "param is error, id not exist"
        elif port <= 0:
            return False, "param is error, port must >0"
        else:
            db_configs_name_list.remove(database_func("database_configs", "get", "first_by_id", id)['name'])
            if name in db_configs_name_list:
                return False, "param is error, name already exist"
            else:
                return True, None
