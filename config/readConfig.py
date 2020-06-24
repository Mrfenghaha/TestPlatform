# -*- coding: utf-8 -
import os
import yaml
# 人称最稳重方法，每加一层os.path.dirname()即向上翻一层,os.getcwd()获取当前目录的绝对路径
# os.getcwd()用于获取执行py文件的位置，例如在根目录执行获取的位置就是根目录，在common下执行就是common路径
# os.path.dirname(os.path.realpath(__file__))是获取包含该执行语句的py文件的绝对路径
cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env_path = os.path.join(cur_path, 'config/env.yaml')


class File:
    def __init__(self, path):
        self.path = path

    def read_yaml_file(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            # 使用load方法将读出的字符串转字典
            content = yaml.full_load(file)
            file.close()
        return content

    def create_yaml_file(self, content):
        # 判断文件是否存在，不存在则创建，并填写默认值
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as file:
                # 写入内容
                file.write(content)
            file.close()

    def create_file(self):
        # 判断文件是否存在，不存在则创建
        if not os.path.exists(self.path):
            os.mkdir(self.path)


contect = "# 数据库环境\nmysql:\nhost: localhost\nport: 3306\nuser: tester\npassword: tester\ndatabase: test_platform\n" \
          "# 加密密码\nencryption_key: test_platform"
File(env_path).create_yaml_file(contect)  # 如果没有env.yaml则自动创建并写入默认值
env_content = File(env_path).read_yaml_file()  # 读取env.yaml
mysql_info = env_content['mysql']  # 获取env.yaml中的mysql数据
encryption_key = env_content['encryption_key']  # 获取env.yaml中的encryption_key数据
