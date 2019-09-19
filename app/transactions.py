#!/usr/bin/env python3

from proto.transaction_pb2 import Transaction
from proto.helpers import shorten_command_name
from iroha import IrohaCrypto, Iroha


class TransactionsPool:
  r"""
  ___  __             __        __  ___    __        __      __   __   __
   |  |__)  /\  |\ | /__`  /\  /  `  |  | /  \ |\ | /__`    |__) /  \ /  \ |
   |  |  \ /~~\ | \| .__/ /~~\ \__,  |  | \__/ | \| .__/    |    \__/ \__/ |___
  """

  def __init__(self, model=None):
    self._txs = []
    self._model = model

  def add(self, transaction=None):
    """
    Adds an empty Transaction to a pool.
    Returns its index.
    """
    new_tx = Transaction()
    self._populate_tx(new_tx)
    if transaction:
      new_tx.CopyFrom(transaction)
    self._txs.append(new_tx)
    return len(self._txs) - 1

  def __len__(self):
    return len(self._txs)

  def __getitem__(self, key):
    self._validate_key(key)
    tx_copy = Transaction()
    tx_copy.CopyFrom(self._txs[key])
    return tx_copy

  def __setitem__(self, key, value):
    self._validate_key(key)
    self._txs[key].CopyFrom(value)

  def __delitem__(self, key):
    self._validate_key(key)
    del self._txs[key]

  def _validate_key(self, key):
    if not isinstance(key, int):
      raise TypeError('index must be an int value')
    length = len(self._txs)
    if key < -1 * length or key > length:
      raise IndexError('index out of bounds {}/{}'.format(key, length))

  def _populate_tx(self, tx):
    tx.payload.reduced_payload.created_time = Iroha.now()
    tx.payload.reduced_payload.quorum = 1


class TransactionViewer:
  r"""
  ___  __             __        __  ___    __                  ___       ___  __
   |  |__)  /\  |\ | /__`  /\  /  `  |  | /  \ |\ |    \  / | |__  |  | |__  |__)
   |  |  \ /~~\ | \| .__/ /~~\ \__,  |  | \__/ | \|     \/  | |___ |/\| |___ |  \
  """

  def __init__(self, transaction: Transaction):
    self._tx = transaction
    self._data = None

  @property
  def data(self):
    if self._data is None:
      self._calc_data()
    return self._data

  def _calc_batch_size(self):
    tx = self._tx
    size = 0
    if tx.payload.HasField('batch'):
      size = len(tx.payload.batch.reduced_hashes)
    return size

  def _get_batch_type(self):
    tx = self._tx
    if not tx.payload.HasField('batch'):
      return ' '
    return {
        0: 'ATOMIC',
        1: 'ORDERED'
    }[tx.payload.batch.type]

  def _shorten_commands_names(self):
    names = []
    for cmd in self._tx.payload.reduced_payload.commands:
      name = shorten_command_name(cmd.DESCRIPTOR.name)
      names.append(name)
    return ' '.join(names)

  def _list_commands(self):
    names = []
    for cmd in self._tx.payload.reduced_payload.commands:
      name = cmd.DESCRIPTOR.name
      names.append(name)
    return names

  def _calc_data(self):
    tx = self._tx
    core = tx.payload.reduced_payload
    self._data = {
        'hash': IrohaCrypto.hash(tx).hex(),
        'timestamp': str(core.created_time),
        'creator': core.creator_account_id,
        'quorum': str(core.quorum),
        'batch': str(self._calc_batch_size()),
        'batch_type': self._get_batch_type(),
        'commands': str(len(tx.payload.reduced_payload.commands)),
        'signatures': str(len(tx.signatures)),
        'brief': self._shorten_commands_names(),
        'full': self._list_commands()
    }


class TransactionsPoolViewer:
  r"""
  ___  __             __        __  ___    __        __      __   __   __                  ___       ___  __
   |  |__)  /\  |\ | /__`  /\  /  `  |  | /  \ |\ | /__`    |__) /  \ /  \ |       \  / | |__  |  | |__  |__)
   |  |  \ /~~\ | \| .__/ /~~\ \__,  |  | \__/ | \| .__/    |    \__/ \__/ |___     \/  | |___ |/\| |___ |  \
  """

  def __init__(self, pool: TransactionsPool):
    self._pool = pool
    self._data = None

  @property
  def data(self):
    if self._data is None:
      self._calc_data()
    return self._data

  def _calc_data(self):
    self._data = []
    for tx in self._pool._txs:
      view = TransactionViewer(tx)
      self._data.append(view.data)
