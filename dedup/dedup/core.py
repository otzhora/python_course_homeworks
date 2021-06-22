import sys
import os
import hashlib
from collections import defaultdict


CHUNK_SIZE = 1024 # size of 1 chunk in bytes
SKIP_INTERVAL = 1024 # number of chunks after which we skip some chunks
SKIP_SIZE = 1024 # number of chunks to skip


def get_chunks(file, offset=0):
    file.seek(offset * CHUNK_SIZE)
    chunks_read = 0
    n_skips = 0

    while (chunk := file.read(CHUNK_SIZE)):
        yield chunk
        if SKIP_INTERVAL == 0:
            continue

        chunks_read += 1
        if chunks_read % SKIP_INTERVAL:
            n_skips += 1
            file.seek((offset + chunks_read + SKIP_SIZE * n_skips) * CHUNK_SIZE)


def get_hash(file_path, partial=False):
    with open(file_path, "rb") as f:
        h = hashlib.sha1()

        if partial:
            h.update(f.read(CHUNK_SIZE))
        else:
            for chunk in get_chunks(f, 1):
                h.update(chunk)

        return h.digest()


def find_duplicates(dir_path):
    size2file = defaultdict(list)
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                file_size = os.path.getsize(file_path)
                size2file[file_size].append(file_path)
            except OSError as e:
                print(f"Error on file: {file_path}, {e}")
                continue

    for size, files in size2file.items():
        if len(files) < 2:
            continue

        partial_index = defaultdict(list) # (hash) -> file_path
        for file_path in files:
            try:
                hash_index = get_hash(file_path, True)
                partial_index[hash_index].append(file_path)
            except OSError as e:
                print(f"Error on file: {file_path}, {e}")
                continue

        hash2file = {}
        for files in partial_index.values():
            if len(files) < 2:
                continue

            for file_path in files:
                try:
                    hash_rem = get_hash(file_path)
                    if hash_rem in hash2file:
                        print(f"found duplicated files: {hash2file[hash_rem]} and {file_path}")
                    else:
                        hash2file[hash_rem] = file_path
                except OSError as e:
                    print(f"Error on file: {file_path}, {e}")
                    continue



if __name__ == "__main__":
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]

    find_duplicates(dir_path)

