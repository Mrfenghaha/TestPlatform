# -*- coding: utf-8 -
import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.read_config import *

'''
所有数据表结果
'''

mysql = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(mysql_info['user'], mysql_info['password'],
                                                             mysql_info['host'], mysql_info['port'],
                                                             mysql_info['database'])
# 创建对象的基类:
Base = declarative_base()
engine = create_engine(mysql)
Session = sessionmaker(bind=engine)


# 将sqlAlchemy查询的结果转换为dict或list
class TypeCast:

    # def to_dict(self):  # 该方法直接获取数据库原始数值,对于一些特殊字符如时间戳无法转换
    #     return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    #
    # Base.to_dict = to_dict

    def to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            # if getattr(self, key) is not None:
            #     result[key] = str(getattr(self, key))
            if type(getattr(self, key)) == datetime.datetime:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    # 配合todict一起使用
    def to_json(self, all_vendors):
        v = [ven.to_dict() for ven in all_vendors]
        return v
