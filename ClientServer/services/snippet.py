import json

import requests

from ClientServer.constants import MANAGEMENT_NODE_URL


def get_file_snippet_content(address: str, filename: str, username: str, path: str, index: int, prefix: str):
    url = f'{address}/file/{filename}'

    data = {
        'username': username,
        'path': path,
        'index': index,
        'prefix': prefix
    }
    response = requests.get(url, data=data)
    response.raise_for_status()

    return response.json()


def get_file_snippet_details(filename: str, user_id: int, index: int):
    url = f'{MANAGEMENT_NODE_URL}/snippet/{filename}/{index}'
    data = {
        'user_id': user_id,
    }

    response = requests.get(url, json=data)
    response.raise_for_status()

    return response.json()
