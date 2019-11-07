from common.helper import Serializer, NotFoundError
from exts import db
from exts import logger


class BaseDao(object):
    def __init__(self, obj):
        self._obj = obj

    def update_(self, _id, **kwargs):
        """
        根据ID更新对象
        :param _id:
        :param kwargs:
        :return:
        """
        obj = self._obj.query.filter_by(id=_id).first()
        if not obj:
            raise NotFoundError("{} id={} Not Found".format(self._obj.__name__, _id))
        for _k, _v in kwargs.items():
            setattr(obj, _k, _v)
        obj.save()
        db.session.commit()

    def search_(self, **kwargs):
        """
        查询对象列表，返回序列化后的数据
        :param kwargs:
        :return:
        """
        objs = self._obj.query.filter_by(**kwargs).all()
        return Serializer.as_dict(objs)

    def limit_search(self, page_num=1, page_size=10, **kwargs):
        """
        查询指定范围的对象列表，返回序列化后的数据，主要是为了分页接口
        :param page_num:
        :param page_size:
        :param kwargs:
        :return:
        """
        start, end = (page_num - 1) * page_size, page_num * page_size
        objs = self._obj.query.filter_by(**kwargs)[start: end]
        return Serializer.as_dict(objs)

    def delete_(self, _id):
        """
        根据ID删除对象
        :param _id:
        :return:
        """
        self._obj.query.filter_by(id=_id).delete()
        db.session.commit()

    def delete_by_condition(self, **kwargs):
        """
        根据条件删除
        :param kwargs:
        :return:
        """
        self._obj.query.filter_by(**kwargs).delete()
        db.session.commit()

    def get_(self, _id):
        """
        获取单个对象，非序列化
        :param _id:
        :return:
        """
        obj = self._obj.query.filter_by(id=_id).first()
        if not obj:
            logger.error("{} id={} Not Found".format(self._obj.__name__, _id))
            raise NotFoundError("{} id={} Not Found".format(self._obj.__name__, _id))
        return obj

    def get_serializer_(self, _id):
        """
        获取单个序列化后的对象
        :param _id:
        :return:
        """
        obj = Serializer.as_dict(self._obj.query.filter_by(id=_id).first())
        if not obj:
            logger.error("{} id={} Not Found".format(self._obj.__name__, _id))
            raise NotFoundError("{} id={} Not Found".format(self._obj.__name__, _id))
        return obj

    def total_(self, **kwargs):
        """
        根据条件获取对象总数
        :param kwargs:
        :return:
        """
        return self._obj.query.filter_by(**kwargs).count()

    def create_(self, **kwargs):
        """
        创建新的对象
        :param kwargs:
        :return:
        """
        obj = self._obj(**kwargs)
        obj.save()
        return obj
