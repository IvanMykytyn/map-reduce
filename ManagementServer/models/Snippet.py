from sqlalchemy import Column, Integer, String, ForeignKey
from ManagementServer.models.db_config import db


class Snippet(db.Model):
    __tablename__ = 'snippets'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    size = Column(Integer, default=0)
    data_node = Column(String(120), nullable=False)
    index = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "file_id": self.file_id,
            "data_node": self.data_node,
            "index": self.index,
            "size": self.size,
        }


def insert_snippet(file_id, data_node, index, size):
    snippet = Snippet(file_id=file_id, data_node=data_node, index=index, size=size)
    db.session.add(snippet)
    db.session.commit()


def get_file_snippets(file_id):
    snippets = Snippet.query.filter_by(file_id=file_id).all()
    snippet_dicts = [snippet.to_dict() for snippet in snippets]
    return snippet_dicts


def db_get_file_snippet(file_id, index: int):
    snippet = Snippet.query.filter_by(file_id=file_id, index=index).first()
    return snippet.to_dict()


def delete_file_snippets(file_id):
    Snippet.query.filter_by(file_id=file_id).delete()
    db.session.commit()
