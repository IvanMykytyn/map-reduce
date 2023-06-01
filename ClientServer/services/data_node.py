import requests

from ClientServer.constants import MANAGEMENT_NODE_URL


def get_all_data_nodes():
    url = f'{MANAGEMENT_NODE_URL}/data-node/all'
    response = requests.get(url)
    return response.json()
