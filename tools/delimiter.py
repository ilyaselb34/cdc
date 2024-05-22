"""
Author: Ilyas El Boujadaini

Content: Definition of a funtion which detects the delimiter of a csv file.
"""


def detect_delimiter(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        first_line = file.readline()
        if ',' in first_line and ';' in first_line:
            raise ValueError("Both ',' and ';' found in the first line. "
                             "Unable to determine the delimiter.")
        elif ',' in first_line:
            return ','
        elif ';' in first_line:
            return ';'
        else:
            raise ValueError("No delimiter found in the first line.")
