import os


def _invalid(message):
    raise ValueError(message)


def persistence_file_path(value: str):
    """
    File path to persist transactions and queries to. Needs to be both readable and
    writable.
    """
    if value:
        if not os.path.exists(value):
            with open(value, "w") as f:
                f.write("{}")
    return value


OPTIONS = [
    persistence_file_path
]
