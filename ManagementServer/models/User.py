from sqlalchemy import Column, Integer, String, Enum

from ManagementServer.models.db_config import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(60), nullable=False)
    password = Column(String(320), unique=True, nullable=False)
    role = Column(Enum('user', name='roles'), nullable=False, default='user')


def add_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_username_by_id(user_id):
    return get_user_by_id(user_id).username


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
