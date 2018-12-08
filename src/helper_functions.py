__author__ = "Aspen Thompson"


def file_path_to_string(path):
    return file_path_to_string_list(path)[0]


def file_path_to_string_list(path):
    return open(path, 'r').read().splitlines()


def file_path_to_int_list(path):
    return [int(line) for line in file_path_to_string_list(path)]


def spaced_file_path_to_int_list(path):
    return [int(i) for i in file_path_to_string(path).split(' ')]
