import os
import shutil
import math
from datetime import time
from os.path import isfile, join
import json
import logging
import zipfile

SizeNames = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")


def create_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def delete_if_exist(path):
    if os.path.exists(path):
        if isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)


def copy_overwrite(item, destination):
    if isfile(item):
        shutil.copyfile(item, destination)
    else:
        shutil.copytree(item, destination)


def get_formatted_size(path):
    convert_size(get_size(path))


def get_size(start_path):
    if isfile(start_path):
        return os.path.getsize(start_path)

    total_size = 0
    for dir_path, dir_names, file_names in os.walk(start_path):
        for f in file_names:
            fp = os.path.join(dir_path, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, SizeNames[i])


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def zip_item(item, zip_path):
    create_dir_if_not_exist(os.path.dirname(zip_path))

    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

    if isfile(item):
        zipf.write(item, os.path.basename(item))
    else:
        for root, dirs, files in os.walk(item):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.join(remove_prefix(root, item), file))
    zipf.close()


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever