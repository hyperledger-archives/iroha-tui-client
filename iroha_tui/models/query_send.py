import grpc
from iroha.endpoint_pb2_grpc import QueryService_v1Stub

from iroha_tui.models.base import BaseModel
from iroha_tui.screens.query_result import QueryResultView
from iroha_tui.models.query_result import QueryResultModel


class QuerySendModel(BaseModel):
    is_skippable = True
    proceed_caption = "View results"
    is_proceed_available = False  # whatever

    def __init__(self, *args, **kwargs):
        self.query = kwargs.pop("query")
        self.address = kwargs.pop("address")
        self.result = None
        super().__init__(*args, **kwargs)

        self.send_query()

    def send_query(self):
        channel = grpc.insecure_channel(self.address)
        stub = QueryService_v1Stub(channel)

        self.result = stub.Find.future(self.query)

    @property
    def log(self):
        log = [f"Sending query to {self.address}"]
        if self.result.done():
            log.append(f"Got code {self.result.code()} ({self.result.details()})")
            if self.result.code() == grpc.StatusCode.OK:
                log.extend(str(self.result.result()).split("\n"))
        return log

    @property
    def is_request_completed(self) -> bool:
        return self.result.done()

    def proceed(self):
        self.go_to(
            QueryResultView,
            QueryResultModel,
            result=self.result.result(),
            address=self.address,
        )

    def retry(self):
        self.send_query()
