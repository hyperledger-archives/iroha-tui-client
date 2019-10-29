from iroha_tui.models.base import BaseModel
from iroha_tui.proto.message import ProtoMessageProxy


class QueryResultModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.result = kwargs.pop("result")
        self.address = kwargs.pop("address")
        super().__init__(*args, **kwargs)

        self.result_proxy = ProtoMessageProxy(self.result)
