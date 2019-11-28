# -*- coding: utf-8 -
from db.public.public import *
'''
database_configs database配置存储表
'''


class DatabaseConfigs(Base, TypeCast):

    # 业务数据库配置表
    __tablename__ = 'database_configs'
    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    name = Column(String(64), nullable=False, comment='名称')
    ip = Column(String(64), nullable=False, comment='数据库IP')
    port = Column(Integer, nullable=False, comment='数据库端口号')
    username = Column(String(255), nullable=False, comment='数据库帐号')
    password = Column(String(255), nullable=False, comment='数据库密码')
    remark = Column(Text, nullable=False, comment='备注')

    def database_configs_func(self, way, *parm):
        time = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        if way == "insert":
            data = parm[0]  # data = {"name": , "ip": , "port": , "username": , "password": , "remark": }
            add_data = DatabaseConfigs(created_at=time, name=data['name'], ip=data['ip'], port=data['port'],
                                       username=data['username'], password=data['password'],
                                       remark=data['remark'])
            session.add(add_data)
            session.commit()
            new_data = add_data.to_dict()  # 获取添加入数据库的所有数据,并转为dict
            session.close()
            return new_data
        elif way == "delete":
            id = parm[0]
            session.query(DatabaseConfigs).filter(DatabaseConfigs.id == id).update({"deleted_at": time})
            session.commit()
            session.close()
        elif way == "update":
            id = parm[0]
            data = parm[1]  # data = {"name": , "ip": , "port": , "username": , "password": , "description": }
            update_data = dict({"updated_at": time}, **data)
            session.query(DatabaseConfigs).filter(DatabaseConfigs.id == id).update(update_data)
            session.commit()
            new_data = session.query(DatabaseConfigs).filter(DatabaseConfigs.id == id).first()
            session.close()
            return new_data.to_dict()
        elif way == "get":
            operation = parm[0]
            if operation == "all_info":
                t = session.query(DatabaseConfigs).filter(DatabaseConfigs.deleted_at == None).all()
                session.close()
                return self.to_json(t)
            elif operation == "specific_num_info":
                start = parm[1]
                num = parm[2]
                t = session.query(DatabaseConfigs).filter(DatabaseConfigs.deleted_at == None).offset(start).limit(num).all()
                session.close()
                return self.to_json(t)
            elif operation == "all_name":
                t = session.query(DatabaseConfigs.name).filter(DatabaseConfigs.deleted_at == None).all()
                session.close()
                return t
            elif operation == "all_id":
                t = session.query(DatabaseConfigs.id).filter(DatabaseConfigs.deleted_at == None).all()
                session.close()
                return t
            elif operation == "first_by_id":
                id = parm[1]
                t = session.query(DatabaseConfigs).filter(DatabaseConfigs.id == id,
                                                          DatabaseConfigs.deleted_at == None).first()
                session.close()
                return t.to_dict()
