# -*- coding: utf-8 -
from urllib import parse
from src.main.mysql.func import *
from src.main.platform.common.ase import *
from src.main.platform.interface.public.public import *


class DBOperationConfigs:

    def get_db_config_list(self, request):
        parm = parse.parse_qs(parse.urlparse(request.url).query)
        parms = {k: v[0] for k, v in parm.items()}
        page = parms.get("page")
        size = parms.get("size")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_db_configs_list(page, size)
        if check_result[0] is True:
            data = Func().get_db_configs_list(int(page), int(size))
            return right_response(data)
        else:
            return error_response(check_result[1])

    def add_db_config(self, request):
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

    def delete_db_config(self, request):
        id = request.json.get("id")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().delete_db_configs(id)
        if check_result[0] is True:
            Func().delete_db_configs(id)
            return right_response(None)
        else:
            return error_response(check_result[1])

    def update_db_config(self, request):
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

    def get_db_configs_list(self, page, size):
        start = (page - 1) * size  # 按照排序从第n个开始(0-*)
        content = database_func("database_configs", "get", "specific_num_info", start, size)  # 根据开始数值
        for c in content:  # 返回数据较少,通过赋值的方式进行
            del c['password'], c['created_at'], c['updated_at'], c['deleted_at']
        total = database_func("database_configs", "get", "all_info_count")  # 获取总条数
        data = {"content": content, "total": total}
        return data

    def add_db_configs(self, name, ip, port, username, password, remark):
        pc = PrpCrypt(encryption_key)
        new_password = pc.encrypt(password)
        data = {"name": name, "ip": ip, "port": port, "username": username, "password": new_password,
                "remark": remark}
        db_data = database_func("database_configs", "insert", data)
        del db_data['created_at'], db_data['updated_at'], db_data['deleted_at'], db_data['username'], db_data['password']
        return db_data

    def delete_db_configs(self, id):
        database_func("database_configs", "delete", id)

    def update_db_configs(self, id, name, ip, port, username, password, remark):
        pc = PrpCrypt(encryption_key)
        new_password = pc.encrypt(password)
        data = {"id": id, "name": name, "ip": ip, "port": port, "username": username, "password": new_password,
                "remark": remark}
        new_data = database_func("database_configs", "update", id, data)
        del new_data['created_at'], new_data['updated_at'], new_data['deleted_at'], new_data['username'], new_data['password']
        return new_data


class CheckParm(DBQuery):

    def get_db_configs_list(self, page, size):
        try:
            page, size = int(page), int(size)
        except:
            return False, "param is error, param not filled or type error"
        if page <= 0 or size <= 0:
            return False, "param is error, page and size must > 0"
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
        elif name == "" or ip == "" or username == "" or password == "":
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
        elif name == "" or ip == "" or username == "" or password == "":
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
