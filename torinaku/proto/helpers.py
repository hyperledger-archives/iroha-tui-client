import re

_OK_LEN = 3

_REPLACEMENTS = {"Ass": "Ast", "Pee": "Peer"}


def _oklen(reducer):
    def wrapper(string):
        if len(string) > _OK_LEN:
            return reducer(string)
        return string

    return wrapper


def _do_replace(piece):
    if piece in _REPLACEMENTS:
        return _REPLACEMENTS[piece]
    return piece


def _remove_non_initial_vowels(string):
    def do(x):
        return re.sub("(?<!^)[aeiou]", "", string, flags=re.I)

    # return do(string)
    xx = do(string)
    if len(xx) < _OK_LEN:
        return string[0:_OK_LEN]
    elif len(xx) > _OK_LEN:
        return xx[0:_OK_LEN]
    else:
        return xx


def add_spaces(string):
    return re.sub(r"([A-Z])", r" \1", string).strip()


@_oklen
def _remove_duplicates(string):
    return re.sub(r"(.+?)\1+", r"\1", string)


@_oklen
def _remove_consonant_duplicates(string):
    return re.sub(r"([qwrtypsdfghjklzxcvbnm]+?)\1+", r"\1", string, flags=re.I)


def shorten_command_name(command_name):
    spaced = add_spaces(command_name)
    pieces = spaced.split(" ")
    shortened_pieces = []
    for p in pieces:
        shortened = p
        shortened = _remove_consonant_duplicates(shortened)
        shortened = _remove_non_initial_vowels(shortened)
        shortened = _remove_duplicates(shortened)
        correct = _do_replace(shortened)
        shortened_pieces.append(correct)
    return "".join(shortened_pieces)


def capitalize_snake_case(s):
    s = s[0].upper() + s[1:]
    # TODO: maybe do that with a regex, seems a bit ineffective
    idx = s.find("_")
    while idx >= 0:
        s = s[:idx] + s[idx + 1].upper() + s[idx + 2:]
        idx = s.find("_")
    return s
