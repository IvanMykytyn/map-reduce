import datetime

from sqlalchemy import Column, Enum, Integer, String, ForeignKey, DateTime, CheckConstraint
from ClientServer.models.db_config import Base

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    file_name = Column(String(50), CheckConstraint('length(file_name) > 3'), nullable=False)
    path = Column(String(600), nullable=False, default='./')
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.datetime.now())
    size = Column(Integer, CheckConstraint('size > 0'), default=0)
