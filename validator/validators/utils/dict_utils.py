def get_nested(data: dict, path: str):

    keys = path.split('.')

    current = data

    for key in keys:

        if key not in current:
            return None

        current = current[key]

    return current
