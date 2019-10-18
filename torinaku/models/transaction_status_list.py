import grpc
from torinaku.models.base import BaseModel
from torinaku.proto.endpoint_pb2 import TxStatusRequest, TxStatus
from torinaku.proto.endpoint_pb2_grpc import CommandService_v1Stub

from torinaku.models.transaction_status import TransactionStatusModel
from torinaku.screens.transaction_status import TransactionStatusView


class TransactionStatusListModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.tx_hashes = kwargs.pop("tx_hashes")
        self.address = kwargs.pop("address")

        super().__init__(*args, **kwargs)

        self.results = {}
        self.request_statuses()

    def request_statuses(self):
        channel = grpc.insecure_channel(self.address)
        stub = CommandService_v1Stub(channel)

        for h in self.tx_hashes:
            request = TxStatusRequest(tx_hash=h)
            self.results[h] = stub.Status.future(request)

    @property
    def statuses(self):
        output = []
        for h, result in self.results.items():
            if result.done():
                if result.code() == grpc.StatusCode.OK:
                    output.append(
                        ((h, "OK", TxStatus.Name(result.result().tx_status)), h)
                    )
                else:
                    output.append(((h, result.code(), ""), h))
            else:
                output.append(((h, "", ""), h))
        return output

    def show_status(self, h):
        tx_status = None
        if self.results[h].code() == grpc.StatusCode.OK:
            tx_status = self.results[h].result()
        self._application.screen_manager.to(
            TransactionStatusView,
            TransactionStatusModel,
            grpc_status=self.results[h].code(),
            tx_status=tx_status,
        )
