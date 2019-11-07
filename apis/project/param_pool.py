class RunningParamPool(object):

    def __init__(self):
        pass

    def get_property(self, param_name):
        res = getattr(self, param_name)()
        return "" if not res else str(res)
