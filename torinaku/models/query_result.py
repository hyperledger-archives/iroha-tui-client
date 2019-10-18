from torinaku.models.base import BaseModel
from torinaku.proto.message import ProtoMessageProxy


class QueryResultModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.result = kwargs.pop("result")
        self.address = kwargs.pop("address")
        super().__init__(*args, **kwargs)

        self.result_proxy = ProtoMessageProxy(self.result)
