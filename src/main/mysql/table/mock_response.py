# -*- coding: utf-8 -
from src.main.mysql.public.public import *
'''
mock_response mock响应存储表
'''


class MockResponse(Base, TypeCast):

    # mock响应表
    __tablename__ = 'mock_response'
    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    mock_id = Column(Integer, nullable=False, comment='mock接口id')
    is_default = Column(Integer, nullable=False, comment='是否是默认返回值')
    name = Column(String(64), nullable=False, comment='响应编码')
    status = Column(String(64), nullable=False, comment='响应状态')
    headers = Column(TEXT, nullable=True, comment='响应信息头,json字符串格式')
    body = Column(TEXT, nullable=True, comment='响应信息,json字符串格式')
    remark = Column(TEXT, nullable=False, comment='响应备注')
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)

    def mock_response_func(self, way, *parm):
        time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        if way == "insert":
            data = parm[0]  # data={"mock_id":,"is_default":,"name":,"status":,"headers":,"body":,"remark":}
            session = Session()
            add_data = MockResponse(created_at=time, mock_id=data['mock_id'], is_default=data['is_default'],
                                    name=data['name'], status=data['status'], headers=data['headers'],
                                    body=data['body'], remark=data['remark'])
            session.add(add_data)
            session.commit()
            new_data = add_data.to_dict()  # 获取添加入数据库的所有数据,并转为dict
            session.close()
            return new_data
        elif way == "delete":
            operation = parm[0]
            if operation == "first_by_id":
                id = parm[1]
                session = Session()
                session.query(MockResponse).filter(MockResponse.id == id).update({"deleted_at": time})
                session.commit()
                session.close()
            elif operation == "all_by_mockId":
                mock_id = parm[1]
                session = Session()
                session.query(MockResponse).filter(MockResponse.mock_id == mock_id).update({"deleted_at": time})
                session.commit()
                session.close()
        elif way == "update":
            operation = parm[0]
            if operation == "first_by_id":
                id = parm[1]
                data = parm[2]  # data={"mock_id":,"is_default":,"name":,"status":,"headers":,"body":,"remark":}
                update_data = dict({"updated_at": time}, **data)
                session = Session()
                session.query(MockResponse).filter(MockResponse.id == id).update(update_data)
                session.commit()
                new_data = session.query(MockResponse).filter(MockResponse.id == id).first()
                session.close()
                return new_data.to_dict()
            elif operation == "isDefault_by_mockId":
                id = parm[1]
                mock_id = parm[2]
                update_data1 = {"updated_at": time, "is_default": 0}
                update_data2 = {"updated_at": time, "is_default": 1}
                session = Session()
                session.query(MockResponse).filter(MockResponse.mock_id == mock_id, MockResponse.is_default == 1).update(update_data1)
                session.query(MockResponse).filter(MockResponse.id == id).update(update_data2)
                session.commit()
                new_data = session.query(MockResponse.id).filter(MockResponse.mock_id == mock_id, MockResponse.is_default == 1).first()
                session.close()
                return new_data
        elif way == "get":
            operation = parm[0]
            if operation == "all_id":
                session = Session()
                t = session.query(MockResponse.id).filter(MockResponse.deleted_at == None).all()
                session.close()
                return t
            elif operation == "all_by_mockId":
                mock_id = parm[1]
                session = Session()
                t = session.query(MockResponse).filter(MockResponse.mock_id == mock_id, MockResponse.deleted_at == None).all()
                session.close()
                return self.to_json(t)
            elif operation == "first_default_by_mockId":
                mock_id = parm[1]
                session = Session()
                t = session.query(MockResponse).filter(MockResponse.mock_id == mock_id, MockResponse.is_default == 1,
                                                       MockResponse.deleted_at == None).first()
                session.close()
                return t.to_dict()
            elif operation == "all_name_by_mockId":
                mock_id = parm[1]
                session = Session()
                t = session.query(MockResponse.name).filter(MockResponse.mock_id == mock_id, MockResponse.deleted_at == None).all()
                session.close()
                return t
            elif operation == "all_id_by_mockId":
                mock_id = parm[1]
                session = Session()
                t = session.query(MockResponse.id).filter(MockResponse.mock_id == mock_id, MockResponse.deleted_at == None).all()
                session.close()
                return t
            elif operation == "first_by_id":
                id = parm[1]
                session = Session()
                t = session.query(MockResponse).filter(MockResponse.id == id, MockResponse.deleted_at == None).first()
                session.close()
                return t.to_dict()

