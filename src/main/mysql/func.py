# -*- coding: utf-8 -
from src.main.mysql.table.mock_servers import *
from src.main.mysql.table.mock_response import *
from src.main.mysql.table.mock_configs import *
from src.main.mysql.table.database_operations import *
from src.main.mysql.table.database_configs import *


# 数据库调用方法统一入口
def database_func(table, way, *parm):
    if table == "mock_servers":
        data = MockServers().mock_servers_func(way, *parm)
        return data
    elif table == "mock_response":
        data = MockResponse().mock_response_func(way, *parm)
        return data
    elif table == "mock_configs":
        data = MockConfigs().mock_configs_func(way, *parm)
        return data
    elif table == "database_configs":
        data = DatabaseConfigs().database_configs_func(way, *parm)
        return data
    elif table == "database_operations":
        data = DatabaseOperations().database_operations_func(way, *parm)
        return data
    else:
        print("不支持此表操作,请添加相应方法")


# 数据库创建初始数据
class DefaultData(MockConfigs):

    def create_mock_configs(self):
        session = Session()
        time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")

        value_list = ["GET", "POST", "HEAD", "PUT", "PATCH", "DELETE"]
        for value in value_list:
            data = {"created_at": time, "parm": 'req_methods', "value": value}
            person = MockConfigs(created_at=data['created_at'], parm=data['parm'], value=data['value'])
            session.add(person)

        value_list = ["100 Continue", "101 Switching Protocols", "102 Processing", "200 OK", "201 Created",
                      "202 Accepted", "203 Non-Authoritative Information", "204 No Content", "205 Reset Content",
                      "206 Partial Content", "300 Multiple Choices", "301 Moved Permanently", "302 Found",
                      "303 See Other", "304 Not Modified", "305 Use Proxy", "306 Unused", "307 Temporary Redirect",
                      "400 Bad Request", "401 Unauthorized", "402 Payment Required", "403 Forbidden", "404 Not Found",
                      "405 Method Not Allowed", "406 Not Acceptable", "407 Proxy Authentication Required",
                      "408 Request Time-out", "409 Conflict", "410 Gone", "411 Length Required",
                      "412 Precondition Failed", "413 Request Entity Too Large", "414 Request-URL Too Large",
                      "415 Unsupported Media Type", "416 Requested range not satisfiable", "417 Expectation Failed",
                      "500 Internal Server Error", "501 Not Implemented", "502 Bad Gateway", "503 Service Unavailable",
                      "504 Gateway Time-out", "505 HTTP Version not supported"]
        for value in value_list:
            data = {"created_at": time, "parm": 'resp_status', "value": value}
            person = MockConfigs(created_at=data['created_at'], parm=data['parm'], value=data['value'])
            session.add(person)

        value_list = [{"value": "$Time_Ymd", "remark": "日期(年月日)"},
                      {"value": "$Time_HMS", "remark": "时间(时分秒)"},
                      {"value": "$Time_YmdHMS", "remark": "时间(年月日时分秒)"},
                      {"value": "$Time_YmdHMSf", "remark": "时间(年月日时分秒毫秒)"},
                      {"value": "$Time_stamp_10", "remark": "10位时间戳"},
                      {"value": "$Time_stamp_13", "remark": "13位时间戳"},
                      {"value": "$Time_utc_cn", "remark": "上海时间utc的标准时间(TZ)"},
                      {"value": "$Time_iso_cn", "remark": "上海时间utc的iso格式(Z)"},
                      {"value": "$Time_utc_in", "remark": "印度时间utc的标准时间(TZ)"},
                      {"value": "$Time_iso_in", "remark": "印度时间utc的iso格式(Z)"},
                      {"value": "$Time_utc_0tz", "remark": "0时区utc的标准时间(TZ)"},
                      {"value": "$Time_iso_0tz", "remark": "0时区utc的iso格式(Z)"},
                      {"value": "$Random_number_0", "remark": "个位随机数"},
                      {"value": "$Random_number_10", "remark": "十位随机数"},
                      {"value": "$Random_number_100", "remark": "百位随机数"},
                      {"value": "$Random_number_1000", "remark": "千位随机数"},
                      {"value": "$Random_number_10000", "remark": "万位随机数"}]
        for value in value_list:
            data = {"created_at": time, "parm": 'replace_param', "value": value['value'], "remark": value['remark']}
            person = MockConfigs(created_at=data['created_at'], parm=data['parm'], value=data['value'],
                                 remark=data['remark'])
            session.add(person)
        session.commit()
        session.close()


if __name__ == '__main__':
    Base.metadata.create_all(engine)  # 创建表结构
    session = Session()
    if session.query(MockConfigs).count() == 0:
        DefaultData().create_mock_configs()  # 插入mock_configs表初始数据
    else:
        pass
    # Base.metadata.drop_all(engine)  # 删除表结构
