import datetime
import traceback

from exts import db
from common.exceptions import DataBaseError


class BaseModelWithoutTime(object):

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            raise DataBaseError(str(e))

    # 添加多条数据
    def save_all(self, *args):
        try:
            db.session.add_all(args)
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            raise DataBaseError(str(e))

    # 删除一条数据
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            raise DataBaseError(str(e))


class BaseModel(BaseModelWithoutTime):
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_time = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now)
