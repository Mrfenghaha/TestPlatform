# -*- coding: utf-8 -
import os
import time
import logging
from config.readConfig import *

# log_path是存放日志的路径
log_path = os.path.join(cur_path, 'logs')
# 如果不存在这个logs文件夹，就自动创建一个
File(log_path).create_file()


class Log:
    def __init__(self):
        # 文件的命名
        self.log_name = os.path.join(log_path, '%s.log' % time.strftime('%Y-%m-%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter('%(asctime)s - 【%(levelname)s】: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def __console(self, level, message):
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


# 接口的log打印设置
def log(*parm):

    if parm[0] == 'request':
        request = parm[1]
        Log().info("[收到请求]  req_url=" + request.url + "  params=" + request.method + "  body=" + str(request.data))
    elif parm[0] == 'response':
        request = parm[1]
        response = parm[2]
        Log().info("[返回结果]  req_url=" + request.url + "  resp_status=" + response.status + "  resp=" + str(response.data))
    else:
        Log().info(parm[0])


if __name__ == "__main__":
    log = Log()
    log.info("---测试开始----")
    log.info("操作步骤1,2,3")
    log.warning("----测试结束----")
