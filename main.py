# -*- coding: utf-8 -
import os
from flask import *
from src.main.platform.interface import *
from src.main.platform.tool.mock_servers import MockServer
app = Flask(__name__)

# 当前脚本所在的文件绝对路径
cur_path = os.path.dirname(os.path.realpath(__file__))
# 将当前路径设置为python的临时环境变量，用于命令执行,需要设置是因为项目存在多处相互调用
os.putenv("PYTHONPATH", cur_path)


# 系统页面
@app.route('/page/<path:url>')
def system_services_page(url):
    return render_template(url + '.html')


# 系统服务接口
@app.route('/api/<path:url>', methods=['GET', 'POST', 'HEAD', 'PUT', 'PATCH', 'DELETE'])
def system_services_api(url):
    log('request', request)
    response = Interface(url, request).api()
    log('response', request, response)
    return response


# mock服务的接口
# 默认string(只能传str字符),int(只能传int字符)、float(只能传float字符)、path(可以接收任意字符串,包括路径带/)、uuid(只能传uuid字符串)
@app.route('/mock/<path:url>', methods=['GET', 'POST', 'HEAD', 'PUT', 'PATCH', 'DELETE'])
def mock_services_api(url):
    log('request', request)
    response = MockServer(url, request).mock_server()
    log('response', request, response)
    return response


# 创建数据库表和初始数据
def create_db_table():
    # 使用os.path.join拼接地址
    case_path = os.path.join(cur_path, "mysql")
    print(os.path.join(case_path, "func.py"))
    os.system('python3 {}'.format(os.path.join(case_path, "func.py")))


if __name__ == '__main__':
    create_db_table()
    app.run(host='0.0.0.0', port=5000, debug=True)
