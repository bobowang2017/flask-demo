# -*- coding: utf-8 -*-
import collections
import functools
import json
import traceback

from tools.exceptions import ErrorReturnData, InputError


def standardize_api_response(func):
    """ Creates a standardized response. This function should be used as a decorator.
    :function: The function decorated should return a dict with one of
    the keys  bellow:
        success -> GET, 200
        error -> Bad Request, 400
        created -> POST, 201
        updated -> PUT, 200
        deleted -> DELETE, 200
        no-data -> No Content, 204
    :returns: json.dumps(response), staus code
    """

    available_result_keys = [
        'success', 'error', 'created', 'updated', 'deleted', 'no-data']

    status_code_and_descriptions = {
        'success': (200, 'Successful Operation'),
        'error': (400, 'Bad Request'),
        'deny': (403, 'Forbidden'),
        'created': (201, 'Successfully created'),
        'updated': (200, 'Successfully updated'),
        'deleted': (200, 'Successfully deleted'),
        'no-data': (204, 'no-data')
    }

    @functools.wraps(func)
    def make_response(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (ErrorReturnData, InputError) as e:
            return response_error_dict(400, str(e), data=json.dump(e.data) if e.data is not None else None)
        # except (ConnectionError, TypeError, BadRequest) as e:
        #     return response_error_dict(500, str(e))
        # except (DevopsNoExistError, DevopsNotFoundError) as e:
        #     return response_error_dict(404, str(e), data=json.dump(e.data) if e.data is not None else None)
        # except DevopsAuthError as e:
        #     return response_error_dict(401, str(e), data=json.dump(e.data) if e.data is not None else None)
        # except DevopsNoAccess as e:
        #     return response_error_dict(403, str(e), data=json.dump(e.data) if e.data is not None else None)
        # except (DevopsInternalError, DevopsNeedRecordError, K8sError, GitError, DevopsGit409, DevopsBusyError) as e:
        #     return response_error_dict(500, str(e), data=json.dump(e.data) if e.data is not None else None)
        # except Exception as e:
        #     traceback.print_exc()
        #     return response_error_dict(500, str(e))
        if result is None:
            return response_error_dict(400, '')
        if not set(available_result_keys) & set(result.keys()):
            raise ValueError('Invalid result key.')


        status_code, description = status_code_and_descriptions[
            next(iter(result.keys()))
        ]
        #
        # status_code = ("status", status_code)
        # description = (
        #     ('description', description) if status_code[1] != 400 else
        #     ('error', description)
        # )
        # resultValue = result.values()
        # # print(next(iter(resultValue))['data'])
        # if len(resultValue) == 1 and isinstance(next(iter(resultValue)), dict) and 'data' in next(iter(resultValue)):
        #     resultValue = next(iter(resultValue))
        #     if 'total' in resultValue:
        #         return collections.OrderedDict(
        #             [("success", True), status_code, description] + list(resultValue.items())), status_code[-1]
        #     else:
        #         return collections.OrderedDict(
        #             [("success", True), status_code, description, ("total", len(resultValue["data"]))] + list(
        #                 resultValue.items())), status_code[-1]
        # else:
        #     data = (
        #         ('data', next(iter(resultValue))) if status_code[1] != 204 else ('data', '')
        #     )
        #     if str(status_code[1]).startswith('2') and isinstance(data, tuple) and len(data) == 2 and isinstance(
        #             data[1], list):
        #         return collections.OrderedDict(
        #             [("success", True), status_code, description, ("total", len(data[1])), data]), status_code[-1]
        #     else:
        #         return collections.OrderedDict([("success", True), status_code, description, data]), status_code[-1]
        return result
    return make_response


def response_error_dict(status, msg, data=None):
    if data is not None:
        return {'status': status, 'msg': msg, 'data': data}, status
    else:
        return {'status': status, 'msg': msg}, status
