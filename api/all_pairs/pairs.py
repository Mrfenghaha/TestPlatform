# -*- coding: utf-8 -
from api.public.public import *
from src.all_pairs import all_pairs


class AllPairs:

    def get_pairs(self, request):
        input = request.json.get("input")

        # 根据参数检查结果判断,如果检查通过则正常处理
        check_result = CheckParm().get_pairs(input)
        if check_result[0] is True:
            data = Func().get_pairs(input)
            return right_response(data)
        else:
            return error_response(check_result[1])


class Func:

    def get_pairs(self, input):
        data = {"ouput": json.dumps(all_pairs(input)).encode('utf-8').decode('unicode_escape')}
        return data


class CheckParm:

    def get_pairs(self, input):
        if type(input) != str:
            return False, "param is error, param not filled or type error"
        else:
            return True, None

