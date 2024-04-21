import sys
import os

IN_FILE_EXTENSION = '.jack'
OUT_FILE_EXTENSION = '.xml'

def get_filename(file_path):
    return file_path.split('/').pop().split(IN_FILE_EXTENSION)[0]

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        for dir_filename in os.listdir(sys.argv[1]):
            if not IN_FILE_EXTENSION in dir_filename: continue
            filename = get_filename(dir_filename)
            # get xml for file
            print(f'{sys.argv[1]}/{filename}{OUT_FILE_EXTENSION}')
    else:
        # get xml for file
        filename = get_filename(sys.argv[1])
        print(f'{sys.argv[1]}/{filename}{OUT_FILE_EXTENSION}')
