import os


def replace_extension(name, ext):
    dir_name, file_name = os.path.split(name)
    file_root, file_ext = os.path.splitext(file_name)
    return '%s.%s' % (file_root, ext)
