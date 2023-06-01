import argparse
import base64
import os
import pickle
import dill
import shutil
import re

import requests
from flask import Flask, request, jsonify, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, help='Port number to run the server on')

args = parser.parse_args()


@app.route('/file', methods=['POST'])
def upload_file():
    username = request.form['username']
    filename = request.form['filename']
    path = request.form['path']
    file = request.files['file']

    chunk_filename = secure_filename(file.filename)

    general_path = f'./storage/{str(args.port)}/{username}/{path}/{filename}/'

    if file:
        if not os.path.exists(general_path):
            os.makedirs(general_path)

        file.save(os.path.join(general_path, chunk_filename))
        # StatusService.init_file(status="success", path=general_path, filename=chunk_filename)
        return jsonify({'message': 'File uploaded successfully'}), 204
    # else:
    #     StatusService.init_file(status="success", path=general_path, filename=chunk_filename)
    #     return jsonify({'message': 'File uploading failed'}), 400


def delete_empty_directories(pre_path, path):
    current_path = path
    directories = path.split(sep="/")
    for curr_index in range(len(directories), 0, -1):
        if not delete_empty_dir(pre_path + current_path):
            break
        if curr_index != 1:
            current_path = current_path.replace('/' + directories[curr_index - 1], '')


def delete_empty_dir(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        if not os.listdir(dir_path):
            os.rmdir(dir_path)
            return True
        else:
            return False
    else:
        return False


@app.route('/file/<filename>', methods=['DELETE'])
def delete_file(filename):
    username = request.form['username']
    path = request.form['path']

    pre_path = f'./storage/{str(args.port)}/{username}/'
    if os.path.exists(pre_path):
        shutil.rmtree(pre_path + path + "/" + filename)
        delete_empty_directories(pre_path, path)
    return jsonify({'message': 'File deleted successfully'}), 200


@app.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    username = request.form['username']
    path = request.form['path']
    index = request.form['index']
    prefix = request.form['prefix']

    pre_path = f'./storage/{str(args.port)}/{username}/{path}'

    with open(f'{pre_path}/{filename}/{prefix}{filename}_{index}.txt', 'r') as f:
        file_data = f.read()
        return jsonify(file_data), 200


@app.route('/calculation/map', methods=['POST'])
def calculate_map():
    data = request.get_json()

    serialized_fn = data['fn']
    mapper_function = dill.loads(base64.b64decode(serialized_fn))

    path = data['path']
    filename = data['filename']
    username = data['username']

    folder_path = f'./storage/{str(args.port)}/{username}/{path}/{filename}'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt') and file_name.startswith(filename):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'r') as file:
                content = file.read()

                mapper_result = mapper_function(content)

                new_filename = f'map-{file_name.split(".")[0]}.txt'

                with open(os.path.join(folder_path, new_filename), 'w') as new_file:
                    new_file.write(mapper_result)

    return '', 200


@app.route('/snippet/shuffle', methods=['POST'])
def upload_shuffled_snippet():
    data = request.get_json()

    username = data['username']
    filename = data['filename']
    index = data['index']
    path = data['path']
    content = data['content']

    general_path = f'./storage/{str(args.port)}/{username}/{path}/{filename}'
    new_filename = f'sh-{filename}_{index}.txt'
    with open(os.path.join(general_path, new_filename), 'w') as new_file:
        new_file.write(content)
    return '', 204


@app.route('/calculation/reduce', methods=['POST'])
def calculate_reduce():
    data = request.get_json()

    serialized_fn = data['fn']
    reducer_function = dill.loads(base64.b64decode(serialized_fn))

    path = data['path']
    filename = data['filename']
    username = data['username']
    # new_filename = data['new_filename']

    folder_path = f'./storage/{str(args.port)}/{username}/{path}/{filename}'
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt') and file_name.startswith(f'sh-{filename}'):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'r') as file:
                content = file.read()

                reducer_result = reducer_function(content)

                new_filename = f'reduce-{file_name.split(".")[0]}.txt'

                with open(os.path.join(folder_path, new_filename), 'w') as new_file:
                    new_file.write(reducer_result)

    return '', 200


# @app.route('/status')
# def data_node_info():
#     memory = psutil.virtual_memory()
#     disk = psutil.disk_usage('/')
#     data_node_stas = {
#         'domain': 'http://127.0.0.1:' + str(args.port),
#         'cpu': psutil.cpu_percent(),
#         'memory': {
#             'total': memory.total >> 20,
#             'available': memory.available >> 20,
#             'used': memory.used >> 20
#         },
#         'disk': {
#             'total': disk.total >> 30,
#             'available': disk.free >> 30,
#             'used': disk.used >> 30
#         }
#     }
#     return jsonify(data_node_stas)


@app.route('/list-of-files/<username>', methods=['GET'])
def list_of_files(username):
    if os.path.exists('./storage/' + str(args.port) + '/' + username):
        files = os.listdir('./storage/' + str(args.port) + '/' + username)
        return jsonify(files), 200
    else:
        return make_response('', 200)


if __name__ == '__main__':
    app.run(port=args.port)
