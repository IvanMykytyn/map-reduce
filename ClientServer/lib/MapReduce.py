import base64
import itertools
import json
import operator
import pickle

import dill
import requests

from ClientServer.constants import MANAGEMENT_NODE_URL


class MapReduce:
    def __init__(self, dfs):
        self.dfs = dfs
        self.addresses = []
        self.file_path = ''
        self.snippets = []

    def calculate(self, filename:str, mapper, reducer, new_filename: str):
        self.proceed_mapper(filename=filename, mapper=mapper)
        self.proceed_shuffle(filename=filename)
        self.proceed_reducer(filename=filename, reducer=reducer, new_filename=new_filename)

    def proceed_mapper(self, filename: str, mapper):
        response = requests.get(f'{MANAGEMENT_NODE_URL}/snippet/{filename}?addressesOnly=1', json={'user_id': self.dfs.user_id})
        response.raise_for_status()

        addresses = response.json()
        self.addresses = addresses
        file_details = requests.get(f'{MANAGEMENT_NODE_URL}/file/{filename}', json={'user_id': self.dfs.user_id})
        file_details.raise_for_status()
        file_details = file_details.json()

        self.file_path = file_details['path']
        data = {
            'fn': base64.b64encode(dill.dumps(mapper)).decode(),
            'username': self.dfs.username,
            'filename': filename,
            'path': self.file_path
        }

        for address in self.addresses:
            requests.post(f'{address}/calculation/map', json=data)

    def proceed_shuffle(self, filename: str):
        resp = requests.get(f'{MANAGEMENT_NODE_URL}/snippet/{filename}', json={
            'user_id': self.dfs.user_id
        })
        resp.raise_for_status()
        snippets = resp.json()
        self.snippets = snippets

        data = []
        for item in self.snippets:
            snippet_index = item['index']
            content: str = self.dfs.get_file_snippet(filename=filename, index=snippet_index, is_mapper=True)
            for line in content.splitlines():
                data.append((line.strip(), snippet_index))

        num_partitions = len(self.snippets)
        partitions = [[] for _ in range(num_partitions)]
        for key, group in itertools.groupby(sorted(data, key=operator.itemgetter(0)), key=operator.itemgetter(0)):
            partition = partitioner(key, num_partitions)
            for _, index in group:
                partitions[partition].append(key)

        for index, item in enumerate(self.snippets):
            new_data = {
                'filename': filename,
                'path': self.file_path,
                'index': item['index'],
                'username': self.dfs.username,
                'content': '\n'.join(partitions[index]),
            }
            requests.post(f'{item["data_node"]}/snippet/shuffle', json=new_data)

    def proceed_reducer(self, filename: str, reducer, new_filename: str):
        data = {
            'fn': base64.b64encode(dill.dumps(reducer)).decode(),
            'username': self.dfs.username,
            'filename': filename,
            'path': self.file_path,
            'new_filename': new_filename
        }

        for address in self.addresses:
            requests.post(f'{address}/calculation/reduce', json=data)


def partitioner(key, num_partitions):
    return hash(key) % num_partitions
