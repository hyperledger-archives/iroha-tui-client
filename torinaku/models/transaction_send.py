import grpc
from iroha import IrohaCrypto

from torinaku.models.base import BaseModel
from torinaku.models.transaction_status_list import TransactionStatusListModel
from torinaku.proto.endpoint_pb2 import TxList
from torinaku.screens.transaction_status_list import TransactionStatusListView
from torinaku.proto.endpoint_pb2_grpc import CommandService_v1Stub


class TransactionSendModel(BaseModel):
    is_skippable = True
    proceed_caption = "View status"

    def __init__(self, *args, **kwargs):
        self.transactions = kwargs.pop("transactions")
        self.address = kwargs.pop("address")
        self.result = None
        super().__init__(*args, **kwargs)

        self.send_transactions()

    def send_transactions(self):
        channel = grpc.insecure_channel(self.address)
        stub = CommandService_v1Stub(channel)

        tx_list = TxList()
        tx_list.transactions.extend(self.transactions)
        self.result = stub.ListTorii.future(tx_list)

    @property
    def log(self):
        log = [f"Sending {len(self.transactions)} transactions to {self.address}"]
        if self.result.done():
            log.append(f"Got code {self.result.code()} ({self.result.details()})")
        return log

    @property
    def is_proceed_available(self) -> bool:
        return self.result.done() and self.result.code() == grpc.StatusCode.OK

    @property
    def is_request_completed(self) -> bool:
        return self.result.done()

    def proceed(self):
        self._application.screen_manager.to(
            TransactionStatusListView,
            TransactionStatusListModel,
            tx_hashes=[IrohaCrypto.hash(x).hex() for x in self.transactions],
            address=self.address,
        )

    def retry(self):
        self.send_transactions()
