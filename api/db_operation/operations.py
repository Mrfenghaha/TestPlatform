# -*- coding: utf-8 -
from api.public.public import *
from db.func import *
from src.db_operation import *
from common.ase import *
from common.config.readConfig import *


class DBOperationOperation:

    def get_db_operation_list(self, request):
        page_num = request.json.get("page_num")
        num = request.json.get("num")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_db_operation_list(page_num, num)
        if check_result[0] is True:
            data = Func().get_db_operation_list(page_num, num)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def add_db_operation(self, request):
        name = request.json.get("name")
        db_id = request.json.get("db_id")
        sql = request.json.get("sql")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().add_db_operation(name, db_id, sql, remark)
        if check_result[0] is True:
            data = Func().add_db_operation(name, db_id, sql, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def delete_db_operation(self, request):
        id = request.json.get("id")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().delete_db_operation(id)
        if check_result[0] is True:
            Func().delete_db_operation(id)
            return right_response(None)
        else:
            return error_response(check_result[1])

    def update_db_operation(self, request):
        id = request.json.get("id")
        name = request.json.get("name")
        db_id = request.json.get("db_id")
        sql = request.json.get("sql")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().update_db_operation(id, name, db_id, sql, remark)
        if check_result[0] is True:
            data = Func().update_db_operation(id, name, db_id, sql, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def execute_db_operation(self, request):
        id = request.json.get("id")
        param = request.json.get("param")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().execute_db_operation(id, param)
        if check_result[0] is True:
            data = Func().execute_db_operation(id, param)
            return right_response(data)
        else:
            return error_response(check_result[1])


class DBQuery:

    def db_query(self):
        # 动态数据库查询,所以写在方法中每次调用每次获取
        db_operations_name_list = []  # 数据操作名称列表
        for db in database_func("database_operations", "get", "all_name"):
            db_operations_name_list.append(db.name)

        db_operation_id_list = []  # 数据操作id列表
        for db in database_func("database_operations", "get", "all_id"):
            db_operation_id_list.append(db.id)

        db_configs_id_list = []  # 数据操作id列表
        for db in database_func("database_configs", "get", "all_id"):
            db_configs_id_list.append(db.id)

        return db_operations_name_list, db_operation_id_list, db_configs_id_list


class Func(DBQuery):

    def get_db_operation_list(self, page_num, num):
        start = (page_num - 1) * num  # 按照排序从第n个开始(0-*)
        data = database_func("database_operations", "get", "specific_num_info", start, num)
        for d in data:  # 返回数据较少,通过赋值的方式进行
            del d['created_at'], d['updated_at'], d['deleted_at']
        return data

    def add_db_operation(self, name, db_id, sql, remark):
        data = {"name": name, "db_id": db_id, "sql": sql, "remark": remark}
        db_data = database_func("database_operations", "insert", data)
        del db_data['created_at'], db_data['updated_at'], db_data['deleted_at']
        return db_data

    def delete_db_operation(self, id):
        database_func("database_operations", "delete", id)

    def update_db_operation(self, id, name, db_id, sql, remark):
        data = {"id": id, "name": name, "db_id": db_id, "sql": sql, "remark": remark}
        new_data = database_func("database_operations", "update", id, data)
        del new_data['created_at'], new_data['updated_at'], new_data['deleted_at']
        return new_data

    def execute_db_operation(self, id, param):
        db = database_func("database_operations", "get", "first_by_id", id)
        db_info = database_func("database_configs", "get", "first_by_id", db['db_id'])
        host = db_info['ip']
        port = db_info['port']
        pc = PrpCrypt(encryption_key)
        user = pc.decrypt(db_info['username'])
        password = pc.decrypt(db_info['password'])
        sql = db['sql']

        result = DBOperation(host, port, user, password).db_operation(sql, param)
        return result


class CheckParm(DBQuery):

    def get_db_operation_list(self, page_num, num):
        if type(page_num) != int or type(num) != int:
            return False, "param is error, param not filled or type error"
        elif page_num <= 0:
            return False, "param is error, page_num must > 0"
        elif num < 0:
            return False, "param is error, num must >= 0"
        else:
            return True, None

    def add_db_operation(self, name, db_id, sql, remark):
        db_operations_name_list = self.db_query()[0]
        db_configs_id_list = self.db_query()[2]

        if type(name) != str or type(db_id) != int or type(sql) != str or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(name) > 64:
            return False, "param is error, param is too long"
        elif name == "" or sql == "" or remark == "":
            return False, "param is error, param cannot be empty"
        elif db_id <= 0:
            return False, "param is error, db_id must > 0"
        elif name in db_operations_name_list:
            return False, "param is error, name already exist"
        elif db_id not in db_configs_id_list:
            return False, "param is error, db_id not exist"
        else:
            return True, None

    def delete_db_operation(self, id):
        db_configs_id_list = self.db_query()[1]

        if type(id) != int:
            return False, "param is error, param not filled or type error"
        elif id < 0:
            return False, "param is error, id must >= 0"
        elif id not in db_configs_id_list:
            return False, "param is error, id not exist"
        else:
            return True, None

    def update_db_operation(self, id, name, db_id, sql, remark):
        db_operation_name_list = self.db_query()[0]
        db_operation_id_list = self.db_query()[1]

        if type(id) != int or type(name) != str or type(db_id) != int or type(sql) != str or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(name) > 64:
            return False, "param is error, param is too long"
        elif name == "" or sql == "" or remark == "":
            return False, "param is error, param cannot be empty"
        elif id not in db_operation_id_list:
            return False, "param is error, id not exist"
        else:
            db_operation_name_list.remove(database_func("database_operations", "get", "first_by_id", id)['name'])
            if name in db_operation_name_list:
                return False, "param is error, name already exist"
            elif db_id <= 0:
                return False, "param is error, db_id must > 0"
            else:
                return True, None

    def execute_db_operation(self, id, param):
        db_operation_id_list = self.db_query()[1]

        if type(id) != int or type(param) != list:
            return False, "param is error, param not filled or type error"
        elif param == []:
            return False, "param is error, param cannot be empty"
        elif id not in db_operation_id_list:
            return False, "param is error, id not exist"
        else:
            return True, None
