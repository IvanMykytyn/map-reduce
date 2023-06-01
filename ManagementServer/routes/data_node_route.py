from flask import request, jsonify, Blueprint

from ManagementServer.models.DataNode import insert_data_node_to_database, delete_data_node_by_id, get_all_data_nodes

data_node_route = Blueprint('route', __name__)


@data_node_route.route('', methods=['POST'])
def insert_data_node():
    address = request.json.get('address', None)
    insert_data_node_to_database(address=address)
    return '', 200


@data_node_route.route('/<data_node_id>', methods=['DELETE'])
def delete_data_node(data_node_id):
    delete_data_node_by_id(data_node_id=data_node_id)
    return '', 200


@data_node_route.route('/all', methods=['GET'])
def get_all_data_nodes_request():
    data_nodes = get_all_data_nodes()
    return jsonify([{'id': data_node.id, 'address': data_node.address} for data_node in data_nodes]), 200
