# 部署说明
## 手动创建数据库及帐号(mysql)
```
mysql -u root -p  #打开、进入数据库
CREATE DATABASE 数据库名 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;  #创建一个数据库用于储存程序产生的数据
USE 数据库名;
CREATE USER 用户名 IDENTIFIED BY '密码';  #创建用户名、密码帐号，用于数据库访问
GRANT ALL PRIVILEGES on 数据库名.* to '用户名'@'localhost';  #授权创建的帐号访问程序数据库
GRANT ALL PRIVILEGES on 数据库名.* to '用户名'@'localhost' identified by '用户密码';  #旧版mysql授权创建的帐号访问程序数据库
FLUSH PRIVILEGES;
```
## 修改数据库配置文件
位置：config/env.yaml  进行相应的数据库信息修改
## 安装python相关包
```
pip3 install -r requirements.txt
```

## 运行程序
```
python3 main.py  # 端口号5000
```