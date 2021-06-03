import shutil


def extract_all(archives, extract_path):
    for filename in archives:
        shutil.unpack_archive(filename, extract_path)
