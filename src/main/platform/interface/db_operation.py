# -*- coding: utf-8 -
from urllib import parse
from src.main.mysql.func import *
from src.main.platform.common.ase import *
from src.main.platform.tool.db_operation import DBOperation as FuncDBOperation
from src.main.platform.interface.public.public import *


class DBOperation:

    def get_db_operation_list(self, request):
        parm = parse.parse_qs(parse.urlparse(request.url).query)
        parms = {k: v[0] for k, v in parm.items()}
        page = parms.get("page")
        size = parms.get("size")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_db_operation_list(page, size)
        if check_result[0] is True:
            data = Func().get_db_operation_list(int(page), int(size))
            return right_response(data)
        else:
            return error_response(check_result[1])

    def add_db_operation(self, request):
        name = request.json.get("name")
        sql = request.json.get("sql")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().add_db_operation(name, sql, remark)
        if check_result[0] is True:
            data = Func().add_db_operation(name, sql, remark)
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
        sql = request.json.get("sql")
        remark = request.json.get("remark")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().update_db_operation(id, name, sql, remark)
        if check_result[0] is True:
            data = Func().update_db_operation(id, name, sql, remark)
            return right_response(data)
        else:
            return error_response(check_result[1])

    def execute_db_operation(self, request):
        db_id = request.json.get("db_id")
        operation_id = request.json.get("operation_id")
        param = request.json.get("param")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().execute_db_operation(db_id, operation_id, param)
        if check_result[0] is True:
            data = Func().execute_db_operation(db_id, operation_id, param)
            return right_response(data)
        else:
            return error_response(check_result[1])


class DBQuery:

    def db_query(self):
        # 动态数据库查询,所以写在方法中每次调用每次获取
        db_operations_name_list = []  # 数据操作名称列表
        for db in database_func("database_operations", "get", "all_name"):
            db_operations_name_list.append(db.name)

        db_operations_id_list = []  # 数据操作id列表
        for db in database_func("database_operations", "get", "all_id"):
            db_operations_id_list.append(db.id)

        db_configs_id_list = []  # 数据库id列表
        for db in database_func("database_configs", "get", "all_id"):
            db_configs_id_list.append(db.id)

        return db_operations_name_list, db_operations_id_list, db_configs_id_list


class Func(DBQuery):

    def get_db_operation_list(self, page, size):
        start = (page - 1) * size  # 按照排序从第n个开始(0-*)
        content = database_func("database_operations", "get", "specific_num_info", start, size)
        for c in content:  # 返回数据较少,通过赋值的方式进行
            del c['created_at'], c['updated_at'], c['deleted_at']
        total = database_func("database_operations", "get", "all_info_count")  # 获取总条数
        data = {"content": content, "total": total}
        return data

    def add_db_operation(self, name, sql, remark):
        data = {"name": name, "sql": sql, "remark": remark}
        db_data = database_func("database_operations", "insert", data)
        del db_data['created_at'], db_data['updated_at'], db_data['deleted_at']
        return db_data

    def delete_db_operation(self, id):
        database_func("database_operations", "delete", id)

    def update_db_operation(self, id, name, sql, remark):
        data = {"id": id, "name": name, "sql": sql, "remark": remark}
        new_data = database_func("database_operations", "update", id, data)
        del new_data['created_at'], new_data['updated_at'], new_data['deleted_at']
        return new_data

    def execute_db_operation(self, db_id, operation_id, param):
        db_info = database_func("database_configs", "get", "first_by_id", db_id)
        host = db_info['ip']
        port = db_info['port']
        user = db_info['username']
        pc = PrpCrypt(encryption_key)
        password = pc.decrypt(db_info['password'])

        operation_info = database_func("database_operations", "get", "first_by_id", operation_id)
        sql = operation_info['sql']

        result = FuncDBOperation(host, port, user, password).db_operation(sql, param)
        return result


class CheckParm(DBQuery):

    def get_db_operation_list(self, page, size):
        try:
            page, size = int(page), int(size)
        except:
            return False, "param is error, param not filled or type error"
        if page <= 0 or size <= 0:
            return False, "param is error, page and size must > 0"
        else:
            return True, None

    def add_db_operation(self, name, sql, remark):
        db_operations_name_list = self.db_query()[0]

        if type(name) != str or type(sql) != str or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(name) > 64:
            return False, "param is error, param is too long"
        elif name == "" or sql == "":
            return False, "param is error, param cannot be empty"
        elif name in db_operations_name_list:
            return False, "param is error, name already exist"
        else:
            return True, None

    def delete_db_operation(self, id):
        db_operations_id_list = self.db_query()[1]

        if type(id) != int:
            return False, "param is error, param not filled or type error"
        elif id not in db_operations_id_list:
            return False, "param is error, id not exist"
        else:
            return True, None

    def update_db_operation(self, id, name, sql, remark):
        db_operations_name_list = self.db_query()[0]
        db_operations_id_list = self.db_query()[1]

        if type(id) != int or type(name) != str or type(sql) != str or type(remark) != str:
            return False, "param is error, param not filled or type error"
        # 写入数据库的数据,根据数据库响应要求设置长度校验
        elif len(name) > 64:
            return False, "param is error, param is too long"
        elif name == "" or sql == "":
            return False, "param is error, param cannot be empty"
        elif id not in db_operations_id_list:
            return False, "param is error, id not exist"
        else:
            db_operations_name_list.remove(database_func("database_operations", "get", "first_by_id", id)['name'])
            if name in db_operations_name_list:
                return False, "param is error, name already exist"
            else:
                return True, None

    def execute_db_operation(self, db_id, operation_id, param):
        db_configs_id_list = self.db_query()[2]
        db_operations_id_list = self.db_query()[1]

        if type(db_id) != int or type(operation_id) != int or type(param) != list:
            return False, "param is error, param not filled or type error"
        elif db_id not in db_configs_id_list:
            return False, "param is error, db_id not exist"
        elif operation_id not in db_operations_id_list:
            return False, "param is error, operation_id not exist"
        else:
            return True, None
