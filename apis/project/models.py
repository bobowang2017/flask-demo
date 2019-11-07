from sqlalchemy import Column, Integer, String, Text, DateTime
from apis.base.base_model import BaseModel
from exts import db


class Project(db.Model, BaseModel):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    code = Column(String(15), nullable=False, unique=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    owner = Column(Integer)
    git_origin = Column(String(255), default='DEFAULT')
    avatar = Column(Text)
    harbor_id = Column(Integer)
    gitlab_group_id = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    def __repr__(self):
        return '<Project %r>' % self.id
