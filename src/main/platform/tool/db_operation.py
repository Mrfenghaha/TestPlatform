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
        connection = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user,
                                     password=self.mysql_password, charset='utf8')  # 连接数据库
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象，并且将结果作为字典返回

        result_num = cursor.execute(sql, parm)  # 执行语句
        # result = cursor.fetchone()  # 获取首行数据
        # result = cursor.fetchmany(2)  # 获取第几条数据
        result = cursor.fetchall()  # 获取所有数据

        connection.commit()  # 提交到数据库，不提交只是模拟的完成，并不会真正更新数据库
        cursor.close()  # 关闭光标对象
        connection.close()  # 关闭数据库连接

        if result_num == 0:
            result_res = {"result_explain": "无需执行或未查到任何结果", "result": result}
        else:
            result_res = {"result_explain": "执行成功", "result": result}
        return result_res

    # 先后执行多条语句
    def db_operation_more(self, group):
        count = []  # 创建一个数组
        for i in group:
            result_res = self.db_operation(i['sql'], i['parm'])
            count.append(result_res)  # 将执行结果写入数组
        return count