import functools
import json
import re
import traceback
from copy import deepcopy
from datetime import datetime as c_datetime
from datetime import date, time
from sqlalchemy import DateTime, Numeric, Date, Time
from flask import Response, request, make_response
from flask_sqlalchemy import Model
from common.exceptions import *
from common.redis_api import redis_cli


def standard_resp(func):
    """
    Creates a standardized response. This function should be used as a decorator.
    :function: The function decorated should return a dict with one of the keys  bellow:
        success -> GET, 200
        error -> Bad Request, 400
        created -> POST, 200
        updated -> PUT, 200
        deleted -> DELETE, 200
        no-data -> No Content, 204
        not-exist -> Not Exist 404
        no-access -> NoAccessError 403
        internal-error -> InternalError 500
        ……
    :returns: json.dumps(response), status code
    """

    @functools.wraps(func)
    def make_response(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (ReturnDataError, InputError) as e:
            return resp_error(400, str(e), data=e.data)
        except AuthFailureError as e:
            return resp_error(401, str(e), data=e.data)
        except NoAccessError as e:
            return resp_error(403, str(e), data=e.data)
        except (NotExistError, NotFoundError) as e:
            return resp_error(404, str(e), data=e.data)
        except (K8sError,) as e:
            return resp_error(40001, str(e))
        except (GitError, GitLabError,) as e:
            return resp_error(40002, str(e))
        except (JenkinsError,) as e:
            return resp_error(40003, str(e))
        except (LdapError,) as e:
            return resp_error(40004, str(e))
        except (HarborError,) as e:
            return resp_error(40005, str(e))
        except (AlertError,) as e:
            return resp_error(40006, str(e))
        except (VDCError,) as e:
            return resp_error(40007, str(e))
        except Exception as e:
            return resp_error(500, str(e))
        res = {"status": 200, "msg": "ok"}
        if isinstance(result, dict) and result.get('total') is not None:
            res.update(result)
        else:
            res["data"] = result
        return Response(json.dumps(res, ensure_ascii=False), content_type='application/json')

    return make_response


def resp_error(status, msg, data=None):
    traceback.print_exc()
    return {'status': status, 'msg': msg, 'data': data}, status


class Serializer(object):
    """
    公共序列化类，将ORM查询的Model转换成dict数据类型
    """

    @staticmethod
    def as_dict(models):
        # 定义需要序列化时间类型列表
        time_type = [c_datetime, DateTime, date, Date, Time, time]

        # 将多Model联合查询对象转化为字典
        def result_to_dict(results):
            return [dict(zip(r.keys(), (convert_datetime(_r) if type(_r) in time_type else _r for _r in r)))
                    for r in results]

        # 将实体类Model转化为字典
        def model_to_dict(_model):
            for col in _model.__table__.columns:
                if isinstance(col.type, DateTime):
                    value = convert_datetime(getattr(_model, col.name))
                elif isinstance(col.type, Numeric):
                    value = float(getattr(_model, col.name))
                else:
                    value = getattr(_model, col.name)
                yield (col.name, value)

        # 对时间类型数据进行转换
        def convert_datetime(value):
            if isinstance(value, (c_datetime, DateTime)):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, (date, Date)):
                return value.strftime("%Y-%m-%d")
            elif isinstance(value, (Time, time)):
                return value.strftime("%H:%M:%S")

        # 如果查询的是实体类集合
        if isinstance(models, list):
            if not models:
                return []
            # 如果是单个实体的查询
            if isinstance(models[0], Model):
                res = []
                for model in models:
                    _model = model_to_dict(model)
                    _res = dict((g[0], g[1]) for g in _model)
                    res.append(_res)
                return res
            # 如果是多model联合查询
            else:
                return result_to_dict(models)
        else:
            if isinstance(models, Model):
                return dict((g[0], g[1]) for g in model_to_dict(models))
            elif models:
                return dict(
                    zip(models.keys(), (convert_datetime(_r) if type(_r) in time_type else _r for _r in models)))
            else:
                return None


def get_from_cache(key):
    """
    从Redis缓存中获取值
    注意：仅适用于直接查询并返回的场景
    :param key: redis对应的key值
    :return:
    """

    def _wrapper(func):
        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            result = redis_cli.get(key)
            if result:
                return result
            return func(*args, **kwargs)

        return __wrapper

    return _wrapper


def hump2underline(camel_str):
    """
    驼峰形式字符串转成下划线形式
    :param camel_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    """
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', camel_str).lower()
    return sub


def underline2hump(underline_str):
    """
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    """
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数
    # 的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), underline_str)
    return sub


def change_to_camel_case(data):
    """
    深度循环遍历data，将key为下划线的改成驼峰
    :param data:
    :return:
    """
    if isinstance(data, dict):
        copy_data = deepcopy(data)
        for _k, _v in copy_data.items():
            data.pop(_k)
            data[underline2hump(_k)] = _v
            change_to_camel_case(_v)
    elif isinstance(data, list):
        for _item in data:
            if isinstance(_item, dict):
                change_to_camel_case(_item)


def result_to_camel_case(fn):
    """
    将返回的结果key值统一转成驼峰的方式
    备注：前端命名采用驼峰，python都是下划线的方式，故前后对接的时候需要转换
    :param fn:
    :return:
    """

    @functools.wraps(fn)
    def _wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        change_to_camel_case(result)
        return result

    return _wrapper


def camel_to_underline_for_dict(data):
    return {hump2underline(k): v for k, v in data.items() if isinstance(k, str)}


def rate_limit(func):
    """
    限流器
    """

    @functools.wraps(func)
    def _limit(*args, **kwargs):
        path, method = request.path, request.method
        rate = redis_cli.get('rate') or 100
        redis_key = f'{path}:{method}'
        counter = redis_cli.get(redis_key)
        if not counter or counter < rate:
            redis_cli.incr_instance(redis_key)
            redis_cli.expire_at(redis_key, 60)
        else:
            return make_response(json.dumps({"code": 500, "msg": '访问请求限制'}), 500)
        return func(*args, **kwargs)

    return _limit
