# -*- coding: utf-8 -
from src.main.mysql.public.public import *
'''
database_operations database操作存储表
'''


class DatabaseOperations(Base, TypeCast):

    # 数据库操作表
    __tablename__ = 'database_operations'
    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    name = Column(String(64), nullable=False, comment='操作名称')
    db_id = Column(Integer, nullable=False, comment='数据库配置表id')
    sql = Column(TEXT, nullable=False, comment='sql语句')
    remark = Column(TEXT, nullable=False, comment='备注')

    def database_operations_func(self, way, *parm):
        time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        if way == "insert":
            data = parm[0]  # data = {"name": , "db_id": , "sql": , "remark": }
            add_data = DatabaseOperations(created_at=time, name=data['name'], db_id=data['db_id'], sql=data['sql'],
                                          remark=data['remark'])
            session.add(add_data)
            session.commit()
            new_data = add_data.to_dict()  # 获取添加入数据库的所有数据,并转为dict
            session.close()
            return new_data
        elif way == "delete":
            id = parm[0]
            session.query(DatabaseOperations).filter(DatabaseOperations.id == id).update({"deleted_at": time})
            session.commit()
            session.close()
        elif way == "update":
            id = parm[0]
            data = parm[1]  # data = {"name": , "db_id": , "sql": , "description": }
            update_data = dict({"updated_at": time}, **data)
            session.query(DatabaseOperations).filter(DatabaseOperations.id == id).update(update_data)
            session.commit()
            new_data = session.query(DatabaseOperations).filter(DatabaseOperations.id == id).first()
            session.close()
            return new_data.to_dict()
        elif way == "get":
            operation = parm[0]
            if operation == "all_info":
                t = session.query(DatabaseOperations).filter(DatabaseOperations.deleted_at == None).all()
                session.close()
                return self.to_json(t)
            elif operation == "specific_num_info":
                start = parm[1]
                num = parm[2]
                t = session.query(DatabaseOperations).filter(DatabaseOperations.deleted_at == None).offset(start).limit(num).all()
                session.close()
                return self.to_json(t)
            elif operation == "all_name":
                t = session.query(DatabaseOperations.name).filter(DatabaseOperations.deleted_at == None).all()
                session.close()
                return t
            elif operation == "all_id":
                t = session.query(DatabaseOperations.id).filter(DatabaseOperations.deleted_at == None).all()
                session.close()
                return t
            elif operation == "first_by_id":
                id = parm[1]
                t = session.query(DatabaseOperations).filter(DatabaseOperations.id == id,
                                                             DatabaseOperations.deleted_at == None).first()
                session.close()
                return t.to_dict()
