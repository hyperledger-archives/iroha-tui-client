from torinaku.models.base import BaseModel
from torinaku.proto.endpoint_pb2 import TxStatus


class TransactionStatusModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.grpc_status = kwargs.pop("grpc_status")
        self.tx_status = kwargs.pop("tx_status", None)
        super().__init__(*args, **kwargs)

    def get_init_data(self):
        return {
            "grpc_status": str(self.grpc_status).split(".")[-1],
            "tx_status": TxStatus.Name(self.tx_status.tx_status),
            "tx_hash": self.tx_status.tx_hash,
            "err_or_cmd_name": self.tx_status.err_or_cmd_name,
            "failed_cmd_index": str(self.tx_status.failed_cmd_index),
            "error_code": str(self.tx_status.error_code),
        }
