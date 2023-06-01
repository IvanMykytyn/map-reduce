import json

from flask import request, jsonify, Blueprint

from ManagementServer.models.File import get_file_by_file_name
from ManagementServer.models.Snippet import insert_snippet, get_file_snippets, db_get_file_snippet

snippet_route = Blueprint('route', __name__)


@snippet_route.route('', methods=['POST'])
def upload_file_snippet():
    data = request.get_json()
    file_id = data['file_id']
    data_node = data['data_node']
    index = data['index']
    size = data['size']

    insert_snippet(file_id=file_id, data_node=data_node, index=index, size=size)
    return '', 200


@snippet_route.route('/<filename>', methods=['GET'])
def get_all_file_snippets(filename):
    data = request.get_json()
    user_id = data['user_id']

    addresses_only = request.args.get('addressesOnly', False)
    file = get_file_by_file_name(file_name=filename, user_id=user_id)
    snippets = get_file_snippets(file_id=file['id'])

    if addresses_only:
        nodes = set()
        for item in snippets:
            nodes.add(item['data_node'])
        snippets = list(nodes)

    json_str = json.dumps(snippets)
    return json_str, 200


@snippet_route.route('/<filename>/<file_index>', methods=['GET'])
def get_file_snippet(filename, file_index):
    data = request.get_json()
    user_id = data['user_id']

    file = get_file_by_file_name(file_name=filename, user_id=user_id)
    snippets = db_get_file_snippet(file_id=file['id'], index=file_index)

    json_str = json.dumps({
        "id": snippets['id'],
        "address": snippets['data_node'],
        "filename": file['file_name'],
        "index": snippets['index'],
        "path": file['path']
    })

    return json_str, 200
