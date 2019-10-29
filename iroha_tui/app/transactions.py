from iroha import IrohaCrypto
from iroha.transaction_pb2 import Transaction
from iroha_tui.proto.helpers import shorten_command_name, capitalize_snake_case
from iroha_tui.proto.commands import ProtoCommandLoader


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
        if tx.payload.HasField("batch"):
            size = len(tx.payload.batch.reduced_hashes)
        return size

    def _get_batch_type(self):
        tx = self._tx
        if not tx.payload.HasField("batch"):
            return " "
        return {0: "ATOMIC", 1: "ORDERED"}[tx.payload.batch.type]

    def _shorten_commands_names(self):
        names = []
        for cmd in self._tx.payload.reduced_payload.commands:
            oneof = cmd.WhichOneof(ProtoCommandLoader.MSG_FIELD)
            name = capitalize_snake_case(oneof)
            name = shorten_command_name(name)
            names.append(name)
        return " ".join(names)

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
            "hash": IrohaCrypto.hash(tx).hex(),
            "timestamp": str(core.created_time),
            "creator": core.creator_account_id,
            "quorum": str(core.quorum),
            "batch": str(self._calc_batch_size()),
            "batch_type": self._get_batch_type(),
            "commands": str(len(tx.payload.reduced_payload.commands)),
            "signatures": str(len(tx.signatures)),
            "brief": self._shorten_commands_names(),
            "full": self._list_commands(),
        }


class TransactionsPoolViewer:
    def __init__(self, pool):
        self._pool = pool
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._calc_data()
        return self._data

    def _calc_data(self):
        self._data = []
        for tx in self._pool:
            view = TransactionViewer(tx)
            self._data.append(view.data)
