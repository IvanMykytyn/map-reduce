import json
import os
import shutil
import uuid

import math
import requests
from werkzeug.utils import secure_filename

from ClientServer.constants import MANAGEMENT_NODE_URL
from ClientServer.services.data_node import get_all_data_nodes


def get_all_user_files(user_id):
    url = f'{MANAGEMENT_NODE_URL}/file/all'
    data = {'user_id': user_id}
    response = requests.get(url, json=data)
    data = json.loads(response.content)

    if response.ok:
        return data
    else:
        raise Exception('Request failed with status code', response.status_code)


def divide_and_upload_snippets(file, filename, path, username, user_id):
    response = requests.get(f'{MANAGEMENT_NODE_URL}/file/config')

    if response.ok:
        file_split_size = response.json()['file_split_size']
    else:
        raise Exception("GET: /file/config failed with status code" + str(response.status_code))

    session_id = str(uuid.uuid4())
    if not os.path.exists('temporary-folder'):
        os.makedirs('temporary-folder')

    if file:
        general_path = './temporary-folder/' + session_id
        os.makedirs(general_path)

    data = file.read()

    file_lines = data.splitlines()

    num_lines = len(file_lines)

    # calculate the number of files to be created
    num_files = math.ceil(num_lines / file_split_size)

    url_addresses = get_all_data_nodes()

    file_size = os.fstat(file.fileno()).st_size
    data = {'file_name': filename, 'path': path, 'user_id': user_id, 'size': file_size}
    response = requests.post(f'{MANAGEMENT_NODE_URL}/file', json=data)

    if not response.ok:
        raise Exception("Failed on upload to management node")
    else:
        file_id = response.json()['id']

    for i in range(num_files):
        # open the file
        file_path = './temporary-folder/' + session_id + '/' + filename + f'_{i}.txt'
        with open(file_path, 'w') as f:
            f.write('\n'.join(file_lines[i * file_split_size:(i + 1) * file_split_size]))

            files = {'file': open(file_path, 'rb')}
            data = {'username': username, 'filename': filename, 'path': path}

            data_node_url = url_addresses[i % len(url_addresses)]['address']
            url = f'{data_node_url}/file'

            response = requests.post(url, files=files, data=data)

            if response.ok:
                snippet_size = file_split_size
                if i == num_files - 1:
                    snippet_size = num_lines % file_split_size

                data = {'file_id': file_id, 'data_node': data_node_url, 'index': i, 'size': snippet_size}
                response = requests.post(f'{MANAGEMENT_NODE_URL}/snippet', json=data)
                if not response.ok:
                    raise Exception(f"Snippet {i} loading failed")
            else:
                raise Exception(f"Snippet {i} loading failed")

    shutil.rmtree('./temporary-folder/' + session_id)

    return 'successfully'


def delete_file_by_filename(filename, user_id):
    manage_url = f'{MANAGEMENT_NODE_URL}/file'
    data = {"user_id": user_id}

    url_addresses = get_all_data_nodes()

    file_data_response = requests.get(f'{manage_url}/{filename}', json=data)
    if file_data_response.ok:
        file = file_data_response.json()
        for url_address in url_addresses:
            url = f'{url_address["address"]}/file/{filename}'
            file_data = {"username": file['username'], 'path': file['path']}

            response = requests.delete(url, data=file_data)
            if response.status_code == 404 or response.status_code == 500:
                return Exception('Server Error')

    response = requests.delete(f'{manage_url}/{filename}', json=data)
    if response.ok:
        return 'successfully'
    else:
        return 'failed'
