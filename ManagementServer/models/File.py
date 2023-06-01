import datetime
import json

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint

from ManagementServer.models.db_config import db

class File(db.Model):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    file_name = Column(String(50), CheckConstraint('length(file_name) > 3'), nullable=False)
    path = Column(String(600), nullable=False, default='./')
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.datetime.now())
    size = Column(Integer, CheckConstraint('size > 0'), default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "path": self.path,
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "size": self.size,
        }


def get_all_user_files_by_user_id(user_id):
    files = File.query.filter_by(user_id=user_id).all()
    file_dicts = [file.to_dict() for file in files]
    return file_dicts


def get_all_user_filenames(user_id):
    filenames = []
    for row in get_all_user_files_by_user_id(user_id):
        filenames.append(row.file_name)
    return filenames


def insert_file_data(file_name, path, user_id, size):
    new_file = File(file_name=file_name, path=path, user_id=user_id, size=size)
    db.session.add(new_file)
    db.session.commit()
    file = File.query.filter_by(file_name=file_name, user_id=user_id).first()
    return file.to_dict()


def get_file_by_file_name(file_name, user_id):
    file = File.query.filter_by(file_name=file_name, user_id=user_id).first()
    return file.to_dict()


def get_file_by_file_id(file_id):
    return File.query.filter_by(id=file_id).first()


def delete_file_by_file_id(file_id, user_id):
    File.query.filter_by(id=file_id, user_id=user_id).delete()
    db.session.commit()
