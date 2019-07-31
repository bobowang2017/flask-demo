from exts import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20))
    sex = db.Column(db.Integer)
    birthday = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.username
