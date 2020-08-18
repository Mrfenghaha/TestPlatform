# -*- coding: utf-8 -
import pymysql


class DBOperation:

    def __init__(self, host, port, user, password):
        self.mysql_host = host
        self.mysql_port = port
        self.mysql_user = user
        self.mysql_password = password

    # 执行基础sql语句
    def db_operation(self, sql, parm):
        try:
            connection = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user,
                                         password=self.mysql_password, charset='utf8')  # 连接数据库
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象，并且将结果作为字典返回
        except:
            return {"status": "执行失败，数据库配置错误", "result": ''}

        # 当传入的参数个数大于sql中%s出现的次数n时,截取传入的参数，保留前n个参数
        if len(parm) >= sql.count('%s'):
            sql_list = list(filter(None, sql.split(';')))  # 按照';'划分并取出""
            count = 0
            operation_list = []
            for sql in sql_list:
                location1 = count
                count += sql.count('%s')
                location2 = count
                operation_list.append({"sql": sql, "parm": parm[location1: location2]})

            # 执行sql语句，所有语句执行成功后才结束
            result_num_list = []
            result_list = []
            for operation in operation_list:
                sql, parm = operation['sql'], operation['parm']
                try:
                    result_num = cursor.execute(sql, parm)  # 执行语句
                    # result = cursor.fetchone()  # 获取首行数据
                    # result = cursor.fetchmany(2)  # 获取第几条数据
                    result = cursor.fetchall()  # 获取所有数据
                    # 收集执行结果
                    result_num_list.append(result_num)
                    if result != ():
                        result_list.append(result)
                except:
                    return {"status": "执行失败，sql语句错误", "result": ''}
            connection.commit()  # 提交到数据库，不提交只是模拟的完成，并不会真正更新数据库
            cursor.close()  # 关闭光标对象
            connection.close()  # 关闭数据库连接

            if result_num_list.count(0) == len(result_num_list):
                return {"status": "执行成功，无需操作或未查到任何结果", "result": ''}
            else:
                return {"status": "执行成功", "result": result_list}
        else:
            return {"status": "执行失败，参数缺失", "result": ''}
