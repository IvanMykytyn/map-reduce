from sqlalchemy import Column, Integer, String

from ManagementServer.models.db_config import db


class DataNode(db.Model):
    __tablename__ = 'data_nodes'

    id = Column(Integer, primary_key=True)
    address = Column(String(200), nullable=False)


def insert_data_node_to_database(address):
    data_node = DataNode(address=address)
    db.session.add(data_node)
    db.session.commit()


def get_data_node_by_id(data_node_id):
    return DataNode.query.filter_by(id=data_node_id).first()


def get_all_data_nodes():
    return DataNode.query.all()


def delete_data_node_by_id(data_node_id):
    DataNode.query.filter_by(id=data_node_id).delete()
    db.session.commit()


