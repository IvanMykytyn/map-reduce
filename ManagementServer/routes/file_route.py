import json
import pickle

from flask import request, jsonify, Blueprint
import io

import math
import os
import shutil
import uuid

import requests
from werkzeug.utils import secure_filename

from ManagementServer.models.DataNode import insert_data_node_to_database, get_all_data_nodes
from ManagementServer.models.File import insert_file_data, get_all_user_files_by_user_id, delete_file_by_file_id, \
    get_file_by_file_name
from ManagementServer.models.Snippet import insert_snippet, delete_file_snippets
from ManagementServer.models.User import get_user_by_username, get_username_by_id

file_route = Blueprint('route', __name__)


@file_route.route('/all', methods=['GET'])
def get_files():
    data = request.get_json()
    user_id = data['user_id']

    files = get_all_user_files_by_user_id(user_id=user_id)
    json_str = json.dumps(files)
    return json_str, 200


@file_route.route('/<filename>', methods=['GET'])
def get_file(filename):
    data = request.get_json()
    user_id = data['user_id']

    file_info = get_file_by_file_name(file_name=filename, user_id=user_id)
    username = get_username_by_id(user_id=user_id)

    file_info['username'] = username
    json_str = json.dumps(file_info)
    return json_str, 200


@file_route.route('/config', methods=['GET'])
def get_config():
    with open('ManagementServer/management-server-config.json', 'r') as f:
        data = json.load(f)
    response = jsonify(data)
    return response, 200


@file_route.route('', methods=['POST'])
def upload_file():
    data = request.get_json()

    file_name = data['file_name']
    path = data['path']
    user_id = data['user_id']
    size = data['size']

    file = insert_file_data(file_name=file_name, path=path, user_id=user_id, size=size)

    return file, 200


@file_route.route('/<filename>', methods=['DELETE'])
def delete_file(filename):
    data = request.get_json()
    user_id = data['user_id']
    print(user_id)

    file = get_file_by_file_name(file_name=filename, user_id=user_id)

    delete_file_snippets(file_id=file['id'])
    delete_file_by_file_id(file_id=file['id'], user_id=user_id)

    return '', 200
