import os
import re


def get_next_file_name(prefix: str, folder: str, extension: str):
    dir_files = [f for f in os.listdir(folder) if re.match(f'{prefix}_\d+\.{extension}', f)]
    file_numbers = [int(re.search(r'\d+', f).group()) for f in dir_files]
    next_file_number = max(file_numbers, default=0) + 1
    return f'{prefix}_{next_file_number}.{extension}'