# 部署说明
## 手动创建数据库及帐号(mysql)
```
mysql -u root -p  #打开、进入数据库
CREATE DATABASE 数据库名 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;  #创建一个数据库用于储存程序产生的数据
CREATE USER 用户名 IDENTIFIED BY '密码';  #创建用户名、密码帐号，用于数据库访问
GRANT ALL PRIVILEGES ON *.* TO '用户名'@'localhost' IDENTIFIED BY '数据库名' WITH GRANT OPTION;  #授权创建的帐号访问程序数据库
FLUSH PRIVILEGES;
```
## 修改数据库配置文件
位置：/db/db_config/config.yaml  进行响应的修改
```
mysql_host: localhost
mysql_port: 3306
mysql_user: xxx
mysql_password: xxx
mysql_database: xxxxx  # 数据库名称
```
## 安装python相关包
```
sudo pip3 install -r requirements.txt
```

## 运行程序
```
python3 main.py  # 端口号5000
```