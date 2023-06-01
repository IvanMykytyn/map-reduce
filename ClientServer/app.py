

from ClientServer.lib.DFS import DFS
from ClientServer.lib.MapReduce import MapReduce


def mapper(content: str):
    lines = content.splitlines()
    words = []
    for line in lines:
        if line:
            words.extend(line.split(' '))

    result = ""
    for word in words:
        if word:
            result += word + "^^1\n"

    return result


def reducer(content: str):
    lines = content.splitlines()
    result = []
    count = 1
    for i in range(1, len(lines)):
        if lines[i] == lines[i - 1]:
            count += 1
        else:
            if count > 1:
                result.append(f"{lines[i - 1].split('^^')[0]}^^{count}")
            else:
                result.append(lines[i - 1])
            count = 1
    if count > 1:
        result.append(f"{lines[-1].split('^^')[0]}^^{count}")
    else:
        result.append(lines[-1])

    return '\n'.join(result)


if __name__ == '__main__':

    dfs = DFS(username='vanyamyk1', user_id=19)

    # dfs.get_file_snippet(filename='test12', index=2)

    map_reduce = MapReduce(dfs=dfs)

    map_reduce.calculate(filename='novel_test', mapper=mapper, reducer=reducer, new_filename='result')
    #
    # with open('novel_test.txt', 'r') as file:
    #     dfs.upload_file(file=file, path='tests/new_test')

    # dfs.delete_file('novel')

    # richard_file = dfs.get_file('Richard')

    # dfs.get_file_snippet()

    # print(dfs.get_list_of_files())
    #
    # files = dfs.get_files_details()
    # print(files[0].__dict__)
    # print(DFS.get_files_details_string(files))



