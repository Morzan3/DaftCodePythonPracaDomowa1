import os
import itertools
import filecmp
from file_hasher import get_hash


def duplicate_finder(topdir=None):
    if topdir is None:
        topdir = os.getcwd()
    data = {}
    hashed_files = set()
    hashes = {}
    for root, dirs, files in os.walk(topdir):
        #print(root, dirs, files)
        for single_file in files:
            f_path = os.path.join(root, single_file)
            size = os.path.getsize(f_path)
            size_list = data.get(size, [])
            size_list.append(f_path)
            if len(size_list) > 1:
                for file_path in size_list:
                    if file_path not in hashed_files:
                        f_hash = get_hash(file_path)
                        size_hash_list = hashes.get(f_hash, [])
                        if file_path not in size_hash_list:
                            size_hash_list.append(file_path)
                        hashes[f_hash] = size_hash_list
                        if len(size_hash_list) > 1:
                            print(
                                'hash {} collision for following files:\n\t{}\n'.format(
                                    f_hash, '\n\t'.join(size_hash_list)
                                )
                            )
            data[size] = size_list

    # TODO Miejsce, w którym nie byłem do końca pewien jak należy dokonać porównania par plików.
    # Najprostrze jest po prostu wygenerowanie wszystkich możliwych par o danym hashu
    # a następnie porównywać każdą z par jednak wtedy może dojść do niepotrzebnego porównania bo
    # jeśli plik A jest taki sam jak plik B a plik B jest taki sam jak plik C to plik A jest taki
    # sam jak plik C i możemy to stwierdzić bez porównania. Nie było jednak pewien czy
    # takie zaimplementowanie porównania było konieczne.
    for files_to_check in hashes.values():
        for file1, file2 in itertools.combinations(files_to_check, 2):
            if filecmp.cmp(file1, file2):
                print('File collision for following files:\n\t{}\n\t{}'.format(file1, file2))

    return data, hashes

def format_dict(my_dict):
    keys = list(my_dict.keys())
    keys.sort()
    entry_format = '\t{}: {}'
    entry_lines = (entry_format.format(k, my_dict[k]) for k in keys)
    return '{}\n{}\n{}'.format('{', '\n'.join(entry_lines), '}')


data, hashes = duplicate_finder('/home/morzan/Desktop/temp-trh-api')
# print(format_dict(data))
# print(format_dict(hashes))
