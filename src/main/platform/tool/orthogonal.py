# -*- coding: utf-8 -

from __future__ import print_function
import re
from allpairspy import AllPairs


class Orthogonal:

    def parse(self, data):
        # 解析/过滤读取的文件成为可识别格式
        parameters = []
        data = re.split('[\n]', data)  # 根据\n拆分字符为list
        for line in data:
            a = line.replace(' ', '')  # 去除每行中的所有空格
            b = a[a.rfind(':', 1) + 1:]  # 去除:前的所有字符
            c = b[b.rfind('：', 1) + 1:]  # 去除：前的所有字符
            d = re.split('[,，]', c)  # 根据,或，符号拆分字符
            parameters.append(d)
        return parameters

    def all_pairs(self, data):
        parameters = self.parse(data)
        result = []
        for i, pairs in enumerate(AllPairs(parameters)):
            res = {"num": i + 1, "pair": pairs}
            result.append(res)
        return result
