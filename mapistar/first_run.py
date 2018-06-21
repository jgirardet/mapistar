import pathlib


def create_directory_tree(static_dir):
    choices = list("0123456789abcdef")
    p = pathlib.Path(static_dir)
    for i in choices.copy():
        (p / i).mkdir()
        for j in choices.copy():
            (p / i / j).mkdir()
