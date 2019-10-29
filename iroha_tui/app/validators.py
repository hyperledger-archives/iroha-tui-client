"""
All the regexes are taken from Iroha source code (field validator)
"""

import re

PATTERNS = {
    "account_name": r"[a-z_0-9]{1,32}",
    "account_id": None,
    "asset_name": r"[a-z_0-9]{1,32}",
    "asset_id": None,
    "role": r"([a-z_0-9]{1,32})",
    "detail_key": r"([A-Za-z0-9_]{1,64})",
    "domain":
    r"(([a-zA-Z]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)",  # noqa
    "ip4":
    r"(^((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3})(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])))",  # noqa
    "peer_address": None,
}

PATTERNS["account_id"] = "{}@{}".format(PATTERNS["account_name"], PATTERNS["domain"])
PATTERNS["asset_id"] = "{}#{}".format(PATTERNS["asset_name"], PATTERNS["domain"])
PATTERNS["peer_address"] = (
    "(({})|({}))".format(PATTERNS["ip4"], PATTERNS["domain"])
    + r":((6553[0-5]|655[0-2]\d|65[0-4]\d\d|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)$)"
)

REGEXES = {key: re.compile(value) for (key, value) in PATTERNS.items()}


def validator(subject, value):
    if subject not in REGEXES:
        raise Exception('Requested validator "{}" does not exist'.format(subject))
    regex = REGEXES[subject]
    return bool(regex.match(value))


def make_validator(subject):
    if subject not in REGEXES:
        raise ValueError(f"Requested validator '{subject}' does not exist")
    regex = REGEXES[subject]

    def _validator(value):
        return bool(regex.match(value))

    return _validator


def account_id_validator(value):
    return validator("account_id", value)


def quorum_validator(value):
    try:
        quorum = int(value)
        if 0 < quorum <= 128:
            return True
    except ValueError:
        pass
    return False


def int_validator(value, low: int, high: int):
    try:
        val = int(value)
        if low <= val <= high:
            return True
    except ValueError:
        pass
    return False


def uint_bit_validator(value, bits: int):
    return int_validator(value, 0, (1 << bits) - 1)


def uint64_validator(value):
    return uint_bit_validator(value, 64)


def uint32_validator(value):
    return uint_bit_validator(value, 32)
