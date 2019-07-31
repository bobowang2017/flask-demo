#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback


class ApiError(Exception):
    def __init__(self, value="unknow reason", op="", data=None):
        self.value = str(value)
        self.data = data
        self.op = str(op)
        if op:
            self.value = "{cls}.{op}: {value}".format(cls=self.__class__.__name__, op=str(self.op),
                                                      value=str(self.value))
        else:
            self.value = "{value}".format(value=str(self.value))
        super().__init__(self.value)

    @property
    def is_exist_error(self):
        if not hasattr(self, "_exist"):
            self._exist = False
        return self._exist

    @property
    def is_not_exist_error(self):
        if not hasattr(self, "_noexist"):
            self._noexist = False
        return self._noexist


class NoAccess(ApiError):
    def __init__(self, value="Forbidden", data=None):
        self.data = data
        super().__init__(value="无访问权限")


class NoExistError(ApiError):
    def __init__(self, value="无数据异常", data=None):
        self._noexist = True
        self.data = data
        super().__init__(value)


class InputError(ApiError):
    def __init__(self, value="输入错误", data=None):
        self.data = data
        if isinstance(value, dict):
            value = "\n".join([str(k) + " " + ".".join(v) for k, v in value.items()])
        super().__init__(value)


class ErrorReturnData(ApiError):
    def __init__(self, value="unknow reason", data=None, op=""):
        ##便于跟踪进一步的错误，错误数据放置data中
        self.data = data
        super().__init__(value, op)


class NeedRecordError(ApiError):
    def __init__(self, value="unknow reason", data=None):
        ##错误需要入库或记录单独的日志，一般用错误发生致状态不可逆时使用。如：
        ##value: 注册xx服务失败，主机xxx连不上
        ##data：因注册xx服务失败且恢复失败，需要手工删除yyy服务
        self.data = data
        super().__init__(value)


class InternalError(ApiError):
    def __init__(self, value="内部错误", data=None):
        ##错误需要入库或记录单独的日志，一般用错误发生致状态不可逆时使用。如：
        ##value: 注册xx服务失败，主机xxx连不上
        ##data：因注册xx服务失败且恢复失败，需要手工删除yyy服务
        self.data = data
        super().__init__(value)


def sufei_debug():
    traceback.print_exc(file=open('/tmp/sufei_debug', 'a+'))
