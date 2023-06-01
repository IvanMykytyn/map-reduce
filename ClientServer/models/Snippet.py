from sqlalchemy import Column, Integer, String, ForeignKey
from ClientServer.models.db_config import Base, Session
from ClientServer.models.File import File


class Snippet(Base):
    __tablename__ = 'snippets'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    size = Column(Integer, default=0)
    data_node = Column(String(120), nullable=False)
    index = Column(Integer, nullable=False)


def insert_snippet(file_id, data_node, index, size):
    session = Session()

    snippet = Snippet(file_id=file_id, data_node=data_node, index=index, size=size)
    session.add(snippet)
    session.commit()


def get_file_snippets(file_id):
    return Snippet.query.filter_by(file_id=file_id)


def delete_file_snippets(file_id):
    session = Session()
    Snippet.query.filter_by(file_id=file_id).delete()
    session.commit()

