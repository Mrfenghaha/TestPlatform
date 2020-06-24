# -*- coding: utf-8 -
import pytest
from src.main.platform.tool.db_operation import *


class TestDBOperation:

    def test_db_operation_01(self):
        sql = "SELECT v_code FROM india_appbackend_test.v_codes where phone = '9999911111'  and is_used = 0 order by id desc"
        parm = []
        data = DBOperation().db_operation(sql, parm)
        assert data['result_explain'] == '执行成功'

    def test_db_operation_02(self):
        sql = "update india_appbackend_test.v_codes set is_used=1 where id=%s"
        parm = ['341']
        data = DBOperation().db_operation(sql, parm)
        assert data['result_explain'] == '执行成功'

    def test_db_operation_more(self):
        parm = [{"sql": "update india_appbackend_test.v_codes set is_used=%s where id=%s", "parm": [0, '341']},
                {"sql": "SELECT v_code FROM india_appbackend_test.v_codes where id=%s", "parm": ['341']}]
        data = DBOperation().db_operation_more(parm)
        assert data[0]['result_explain'] == '执行成功'
        assert data[1]['result_explain'] == '执行成功'


if __name__ == '__main__':
    pytest.main()
