from typing import List

from iroha import IrohaCrypto, Iroha

from torinaku.models.base import BaseModel

from torinaku.models.transaction_send import TransactionSendModel
from torinaku.models.transaction_editor import TransactionEditorModel
from torinaku.models.signature_picker import SignaturePickerModel
from torinaku.models.peer_picker import PeerPickerModel
from torinaku.models.transaction_status_list import TransactionStatusListModel
from torinaku.models.batch_type_selector import BatchTypeSelectorModel
from torinaku.screens.transaction_status_list import TransactionStatusListView
from torinaku.screens.transaction_editor import TransactionEditorView
from torinaku.screens.grpc_request import GrpcRequestView
from torinaku.screens.signature_picker import SignaturePickerView
from torinaku.screens.peer_picker import PeerPickerView
from torinaku.screens.selector import SelectorView


class TransactionListModel(BaseModel):
    @property
    def transactions(self):
        return self._application.transactions

    def main_menu(self):
        self._application.screen_manager.back()

    def send_txs(self, tx_idxs: List[int]):
        self._application.screen_manager.to(
            PeerPickerView,
            PeerPickerModel,
            on_peer_chosen=self._make_send_tx_callback(tx_idxs),
        )

    def _make_send_tx_callback(self, tx_idxs: List[int]):
        def send_tx_callback(address: str):
            transactions = [self._application.transactions[i] for i in tx_idxs]
            self._application.screen_manager.to(
                GrpcRequestView,
                TransactionSendModel,
                transactions=transactions,
                address=address,
            )

        return send_tx_callback

    def get_tx_statuses(self, tx_idxs: List[int]):
        self._application.screen_manager.to(
            PeerPickerView,
            PeerPickerModel,
            on_peer_chosen=self._make_tx_status_callback(tx_idxs),
        )

    def _make_tx_status_callback(self, tx_idxs: List[int]):
        def tx_status_callback(address: str):
            transactions = [self._application.transactions[i] for i in tx_idxs]
            tx_hashes = [IrohaCrypto.hash(x).hex() for x in transactions]
            self._application.screen_manager.to(
                TransactionStatusListView,
                TransactionStatusListModel,
                tx_hashes=tx_hashes,
                address=address,
            )

        return tx_status_callback

    def batch_txs(self, tx_idxs: List[int]):
        self._application.screen_manager.to(
            SelectorView,
            BatchTypeSelectorModel,
            on_type_selected=self._make_batch_type_callback(tx_idxs),
        )

    def _make_batch_type_callback(self, tx_idxs: List[int]):
        def batch_type_callback(is_atomic: bool):
            transactions = [self._application.transactions[i] for i in tx_idxs]
            Iroha.batch(transactions, is_atomic)
            for i in tx_idxs:
                self._application.transactions[i].CopyFrom(transactions[i])

        return batch_type_callback

    def sign_txs(self, tx_idxs: List[int]):
        self._application.screen_manager.to(
            SignaturePickerView,
            SignaturePickerModel,
            on_private_key_entered=self._make_sign_tx_callback(tx_idxs),
        )

    def _make_sign_tx_callback(self, tx_idxs: List[int]):
        def sign_tx_callback(private_key):
            for i in tx_idxs:
                transaction = self._application.transactions[i]
                signed_transaction = IrohaCrypto.sign_transaction(
                    transaction, private_key
                )
                transaction.CopyFrom(signed_transaction)

        return sign_tx_callback

    def create_tx(self):
        self._application.screen_manager.to(
            TransactionEditorView, TransactionEditorModel
        )

    def edit_tx(self, idx):
        self._application.screen_manager.to(
            TransactionEditorView,
            TransactionEditorModel,
            transaction=self.transactions[idx],
        )

    def _batch_summary(self):
        result = "Non-batched transaction"
        if not self._model._temp_tx.payload.HasField("batch"):
            return result
        batch_type = {0: "ATOMIC", 1: "ORDERED"}[
            self._model._temp_tx.payload.batch.type
        ]
        count = len(self._model._temp_tx.payload.batch.reduced_hashes)
        return "{} batch of {} transactions".format(batch_type, count)
