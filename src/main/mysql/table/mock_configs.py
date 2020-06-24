# -*- coding: utf-8 -
from src.main.mysql.public.public import *
'''
mock_configs mock参数配置表
'''


class MockConfigs(Base, TypeCast):

    # mock配置表(请求、响应的数据读取)
    __tablename__ = 'mock_configs'
    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    parm = Column(String(25), nullable=False, comment='参数名称:请求方法,响应状态')
    value = Column(String(64), nullable=False, comment='参数值')
    remark = Column(TEXT, nullable=True, comment='参数备注')

    def mock_configs_func(self, way, *parm):
        if way == "get":
            operation = parm[0]
            if operation == "all_value_by_parm":
                parm = parm[1]
                t = session.query(MockConfigs.value).filter(MockConfigs.parm == parm,
                                                            MockConfigs.deleted_at == None).all()
                session.close()
                return t
            elif operation == "all_value_remark_by_parm":
                parm = parm[1]
                t = session.query(MockConfigs.value, MockConfigs.remark).filter(MockConfigs.parm == parm,
                                                                                MockConfigs.deleted_at == None).all()
                session.close()
                return t
