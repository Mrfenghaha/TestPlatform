# -*- coding: utf-8 -
import os
import yaml


# 人称最稳重方法，每加一层os.path.dirname()即向上翻一层,os.getcwd()获取当前目录的绝对路径
# os.getcwd()用于获取执行py文件的位置，例如在根目录执行获取的位置就是根目录，在common下执行就是common路径
# os.path.dirname(os.path.realpath(__file__))是获取包含该执行语句的py文件的绝对路径
cur_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(cur_path, 'env.yaml')

# 如果没有config/env.yaml,自动创建并写入默认值
if not os.path.exists(config_path):
    os.mknod(config_path)  # 创建env.yaml文件
    with open(config_path, 'w') as file:
        file.write('# 加密密码'
                   'encryption_key: xxxxxx')


with open(config_path, 'r', encoding='utf-8') as file:
    # 使用load方法将读出的字符串转字典
    data_content = yaml.full_load(file)

encryption_key = data_content['encryption_key']
