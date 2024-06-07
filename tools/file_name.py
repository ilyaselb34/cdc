import re
import os


def exit_file_name(file_name: str):

    # Expression régulière pour capturer tout ce qui est entre "Enedis" et
    # ".csv", inclusivement
    pattern = r'(Enedis.*?\.csv)'

    # Recherche de la correspondance dans la chaîne
    match = re.search(pattern, file_name)

    if match:
        result = match.group(1)
        exit_path = os.path.join('output', result[:-4] + '_cleaned.csv')
        return exit_path
    else:
        return 'No match found'
