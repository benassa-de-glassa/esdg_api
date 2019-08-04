import string

def sanitize(text):
    replace_chars = [' ', ]
    for char in replace_chars:
        text = string.replace(text, '_')

    return text