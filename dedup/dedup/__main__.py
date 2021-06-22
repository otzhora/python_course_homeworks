import sys

from dedup import find_duplicates


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]

    find_duplicates(dir_path)
