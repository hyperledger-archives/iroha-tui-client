"""
All the regexes are taken from Iroha source code (field validator)
"""

import re

PATTERNS = {
    'account_name': r'[a-z_0-9]{1,32}',
    'account_id': None,
    'asset_name': r'[a-z_0-9]{1,32}',
    'asset_id': None,
    'role': r'([a-z_0-9]{1,32})',
    'detail_key': r'([A-Za-z0-9_]{1,64})',
    'domain': r'(([a-zA-Z]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)',
    'ip4': r'(^((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3})(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])))',
    'peer_address': None
}

PATTERNS['account_id'] = '{}@{}'.format(PATTERNS['account_name'], PATTERNS['domain'])
PATTERNS['asset_id'] = '{}#{}'.format(PATTERNS['asset_name'], PATTERNS['domain'])
PATTERNS['peer_address'] = '(({})|({}))'.format(PATTERNS['ip4'], PATTERNS['domain']) + \
    r':((6553[0-5]|655[0-2]\d|65[0-4]\d\d|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)$)'

REGEXES = {key: re.compile(value) for (key, value) in PATTERNS.items()}


def validator(subject, value):
  if subject not in REGEXES:
    raise Exception('Requested validator "{}" does not exist'.format(subject))
  regex = REGEXES[subject]
  return bool(regex.match(value))


def account_id_validator(value):
  return validator('account_id', value)


def quorum_validator(value):
  try:
    quorum = int(value)
    if 0 < quorum <= 128:
      return True
  except:
    pass
  return False


def uint64_validator(value):
  try:
    val = int(value)
    if 0 <= val <= (2**64 - 1):
      return True
  except:
    pass
  return False
