from datetime import datetime

from iroha import IrohaCrypto, Iroha

from torinaku.models.base import BaseModel
from torinaku.screens.selector import SelectorView
from torinaku.screens.command_editor import CommandEditorView
from torinaku.screens.signature import SignatureView
from torinaku.screens.signature_picker import SignaturePickerView
from torinaku.models.signature import SignatureModel
from torinaku.models.signature_picker import SignaturePickerModel
from torinaku.models.command_editor import CommandEditorModel
from torinaku.models.command_type_selector import CommandTypeSelectorModel
from torinaku.proto.transaction_pb2 import Transaction
from torinaku.proto.message import ProtoMessageProxy
from torinaku.proto.commands import ProtoCommandLoader
from torinaku.app.validators import uint64_validator


class DateUtils:
    @staticmethod
    def now_ts():
        """Timestamp in milliseconds"""
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def epochms_to_human(timestamp):
        """Return locale’s appropriate date and time representation."""
        ts = int(timestamp)
        millis = ts % 1000
        dt = datetime.fromtimestamp(int(ts) / 1000)
        return dt.strftime("%c {:03d}ms".format(millis))


class TransactionEditorModel(BaseModel):
    _plain_fields = [
        ".payload.reduced_payload.creator_account_id",
        ".payload.reduced_payload.created_time",
        ".payload.reduced_payload.quorum",
    ]

    def __init__(self, *args, **kwargs):
        self.target_transaction = kwargs.pop("transaction", None)
        self.is_tx_valid = True

        self.transaction = Transaction()
        self.transaction.payload.reduced_payload.created_time = Iroha.now()
        self.transaction.payload.reduced_payload.quorum = 1

        self.tx_proto_proxy = ProtoMessageProxy(self.transaction)
        if self.target_transaction:
            self.transaction.CopyFrom(self.target_transaction)

        super().__init__(*args, **kwargs)

    def get_init_data(self):
        return {
            field: str(self.tx_proto_proxy.read(field)) for field in self._plain_fields
        }

    def validate_timestamp(self, value):
        if not uint64_validator(value):
            return False
        try:
            DateUtils.epochms_to_human(value)
            return True
        except Exception:
            pass
        return False

    def set_timestamp_to_now(self):
        self.transaction.payload.reduced_payload.created_time = DateUtils.now_ts()

    def update_data(self, frame_data):
        for field in self._plain_fields:
            self._data[field] = frame_data[field]
        try:
            for field in self._plain_fields:
                self.tx_proto_proxy.set_to(field, frame_data[field])
            self.is_tx_valid = True
        except ValueError:
            self.is_tx_valid = False

        self._update_tx_hash()
        self._update_command_names()
        self._update_batch_summary()
        self._update_signatures()
        self._update_human_time()

    def _update_tx_hash(self):
        h = IrohaCrypto.hash(self.transaction).hex()
        if not self.is_tx_valid:
            h += " <invalid protobuf data>"
        self._data["tx_hash"] = h

    def _update_command_names(self):
        commands = self.transaction.payload.reduced_payload.commands
        command_names = []
        for i, cmd in enumerate(commands):
            command_name = cmd.WhichOneof(ProtoCommandLoader.MSG_FIELD)
            command_names.append((f"{i} - {command_name}", i))
        self._data["command_names"] = command_names

    def _update_signatures(self):
        signatures = self.transaction.signatures
        signature_titles = [(s.signature, i) for i, s in enumerate(signatures)]
        self._data["signatures"] = signature_titles

    def _update_batch_summary(self):
        """
        Produce a summary message about this transaction's participation in a batch
        (or lack thereof).
        """

        if not self.transaction.payload.HasField("batch"):
            self._data["batch_summary"] = "Non-batched transaction"
            return

        batch_type = {0: "ATOMIC", 1: "ORDERED"}[self.transaction.payload.batch.type]
        count = len(self.transaction.payload.batch.reduced_hashes)

        summary = f"{batch_type} batch of {count} transactions"
        self._data["batch_summary"] = summary

    def _update_human_time(self):
        self._data["human_time"] = DateUtils.epochms_to_human(
            self.transaction.payload.reduced_payload.created_time
        )

    def add_command(self):
        self._application.screen_manager.to(
            SelectorView, CommandTypeSelectorModel, transaction=self.transaction
        )

    def edit_command(self, idx):
        self._application.screen_manager.to(
            CommandEditorView,
            CommandEditorModel,
            command=self.transaction.payload.reduced_payload.commands[idx],
        )

    def remove_command(self, idx):
        del self.transaction.payload.reduced_payload.commands[idx]

    def add_signature(self):
        self._application.screen_manager.to(
            SignaturePickerView,
            SignaturePickerModel,
            on_private_key_entered=self._sign_tx_with_private_key,
        )

    def remove_signature(self, idx):
        del self.transaction.signatures[idx]

    def show_signature(self, idx):
        self._application.screen_manager.to(
            SignatureView, SignatureModel, signature=self.transaction.signatures[idx]
        )

    def _sign_tx_with_private_key(self, private_key: str):
        self.transaction = IrohaCrypto.sign_transaction(self.transaction, private_key)

    def save(self):
        """
        Save the underlying form, resulting either in creation of a new
        transaction, or in modifying the passed-in-one.
        """
        if self.target_transaction is not None:
            self.target_transaction.CopyFrom(self.transaction)
        else:
            self._application.transactions.insert(0, self.transaction)

    def save_go_back(self):
        """
        Save and go to the previous screen.
        """
        self.save()
        self.cancel()
