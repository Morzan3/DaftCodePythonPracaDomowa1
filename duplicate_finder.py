import os
import itertools
import filecmp
from pprint import pprint
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

    for files_to_check in hashes.values():
        file_corelation = {}
        for file in files_to_check:
            file_corelation[file] = set()

        # Dla każdego hasha tworzę słownik {lokalizaja pliku: set plików z którymi jest powiązany)
        # Tworzę wszystkie możliwe pary plików i po kolei sprawdzam:
        # jeśli plik2 znajduje się w zbiorze wartości pliku1 to nie musze sprawdzać tylko pisze, że zachodzi kolizja
        # jesli nie znajduje się w zbiorze to porówuje te pliki.
        # W przypadku gdy pliki są identyczne to dodaję plik2 to setu pliku1, dodaję wszystkie pliki powiązane z plikiem 2
        # do setu pliku1 a następnie wszystkie te wartości kopiuje do setów plików pokrewnych do pliku1.
        # Rozwiązanie wydaje mi się dosyć zawiłe więc chętnie poznał bym jakieś lepsze :)

        for file1, file2 in itertools.combinations(files_to_check, 2):
            if file2 not in file_corelation[file1]:
                if filecmp.cmp(file1, file2):
                    file_corelation[file1].add(file2)
                    if file_corelation[file2]:
                        file_corelation[file1] = file_corelation[file1].union(file_corelation[file2])

                    for file in file_corelation[file1]:
                        file_corelation[file] = file_corelation[file].union(file_corelation[file1])

                    file_corelation[file2].add(file1)

                    print('File collision for following files:\n\t{}\n\t{}'.format(file1, file2))

            else:
                print('File collision for following files:\n\t{}\n\t{}'.format(file1, file2))

        pprint(file_corelation)

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
