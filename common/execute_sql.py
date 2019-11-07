from exts import db
from sqlalchemy import text


def dict_fetchall(sql, params):
    """
    执行原生SQL语句的查询操作
    :param sql: SQL语句  sql = 'select * from user where id = :id'
    :param params: SQL参数 {'id':1}
    :return: list
    """
    handler = db.session.execute(text(sql), params)
    desc = handler.cursor.description
    handler.cursor.close()
    return [dict(zip([col[0] for col in desc], row)) for row in handler.fetchall()]
