import requests

from ClientServer.constants import MANAGEMENT_NODE_URL
from ClientServer.services.file import get_all_user_files


class FileDetails:
    def __init__(self, filename, path, size):
        self.filename = filename
        self.path = path
        self.size = size

    def __str__(self):
        return f'path: {self.path}\nfilename: {self.filename}\nsize: {self.size}'


def get_all_user_filenames(user_id):
    filenames = []
    for row in get_all_user_files(user_id):
        filenames.append(row['file_name'])
    return filenames


def get_all_files(user_id):
    files = []
    for row in get_all_user_files(user_id):
        files.append(FileDetails(row['file_name'], row['path'], row['size']))
    return files


#
# def insert_file_data(file_name, path, user_id, size):
#
#     session = Session()
#     new_file = File(file_name=file_name, path=path, user_id=user_id, size=size)
#     session.add(new_file)
#     session.commit()
#     return File.query.filter_by(file_name=file_name, user_id=user_id).first()
#

#
# def get_file_by_file_name(file_name, user_id):
#     return File.query.filter_by(file_name=file_name, user_id=user_id).first()
#
#
# def get_file_by_file_id(file_id):
#     return File.query.filter_by(id=file_id).first()
#
#
# def delete_file_by_file_id(file_id, user_id):
#     session = Session()
#     File.query.filter_by(id=file_id, user_id=user_id).delete()
#     session.commit()



def build_file_hierarchy(file_details_list):
    paths = {}
    for file_details in file_details_list:
        path_parts = file_details.path.split('/')
        current_path = paths
        for part in path_parts:
            current_path = current_path.setdefault(part, {})
        current_path[file_details.filename] = file_details.size
    return _build_file_details_string_helper(paths, 0)


def _build_file_details_string_helper(path_dict, indent_level):
    output = ''
    for path, details in path_dict.items():
        output += ' ' * (indent_level * 2) + path
        if isinstance(details, dict):
            output += '/' + '\n'
            output += _build_file_details_string_helper(details, indent_level + 1)
        else:
            output += f' - {details}\n'
    return output
