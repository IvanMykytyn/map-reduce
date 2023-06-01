import io

import requests
from werkzeug.utils import secure_filename

from ClientServer.services.data_node import get_all_data_nodes
from ClientServer.helpers.file import get_all_user_filenames, build_file_hierarchy, get_all_files
from ClientServer.services.file import divide_and_upload_snippets, delete_file_by_filename
from ClientServer.services.snippet import get_file_snippet_details, get_file_snippet_content


class DFS:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def get_list_of_files(self):
        return get_all_user_filenames(self.user_id)

    def get_files_details(self):
        return get_all_files(self.user_id)

    @staticmethod
    def get_files_details_string(files):
        return build_file_hierarchy(files)

    def upload_file(self, file, path):
        if not file:
            raise Exception("File is required")

        filename = secure_filename(file.name).split('.')[0]

        list_of_files = self.get_list_of_files()

        if filename in list_of_files:
            raise Exception('File with such a name already exists')

        divide_and_upload_snippets(file=file, filename=filename, path=path, username=self.username, user_id=self.user_id)

        return "successful"

    def delete_file(self, filename):
        list_of_files = self.get_list_of_files()

        if filename in list_of_files:
            delete_file_by_filename(filename=filename, user_id=self.user_id)
            return 'successful'
        else:
            raise Exception('No file with such a name')

    def get_file_snippet(self, filename: str, index: int, is_mapper: bool = False, is_reducer: bool = False):
        snippet_details = get_file_snippet_details(filename=filename, user_id=self.user_id, index=index)

        address = snippet_details['address']
        filename = snippet_details['filename']
        path = snippet_details['path']
        index = snippet_details['index']

        prefix = ''
        if is_mapper:
            prefix = 'map-'
        elif is_reducer:
            prefix = 'reduce-'

        snippet_content = get_file_snippet_content(address=address,
                                                   filename=filename, username=self.username,
                                                   path=path, index=index, prefix=prefix)
        return snippet_content



        # file_snippets = []
        # for snippet in snippets:
        #     data = {'username': self.username, 'index': snippet.index, 'path': file.path}
        #     url = f'{snippet.data_node}/file/{filename}'
        #     response = requests.get(url, data=data).json()
        #     file_data = response['file_data']
        #     file_snippets.append(file_data)
        #
        # self.delete_file(filename)
        #
        # return io.StringIO('\n'.join(file_snippets))

