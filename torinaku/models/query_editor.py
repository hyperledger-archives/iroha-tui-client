from iroha import Iroha, IrohaCrypto
from iroha.queries_pb2 import Query
from loguru import logger

from torinaku.models.base import BaseModel

from torinaku.proto.message import ProtoMessageProxy
from torinaku.proto.queries import ProtoQueryLoader

from torinaku.screens.peer_picker import PeerPickerView
from torinaku.screens.signature_picker import SignaturePickerView
from torinaku.screens.grpc_request import GrpcRequestView

from torinaku.models.peer_picker import PeerPickerModel
from torinaku.models.signature_picker import SignaturePickerModel
from torinaku.models.query_send import QuerySendModel


class QueryEditorModel(BaseModel):
    _plain_fields = [
        ".payload.meta.created_time",
        ".payload.meta.query_counter",
        ".payload.meta.creator_account_id",
    ]

    def __init__(self, *args, **kwargs):
        self.target_query = kwargs.pop("query", None)

        self.query = Query()
        self.query.payload.meta.created_time = Iroha.now()

        self.query_proto_proxy = ProtoMessageProxy(self.query)
        if self.target_query:
            self.query.CopyFrom(self.target_query)
        logger.debug(self.query)

        self.is_query_valid = False
        self.payload_proxy = None

        queries = ProtoQueryLoader().queries
        self.query_type_options = [(x[0], x[2]) for x in queries]
        if self.target_query:
            self.default_query_type = self.query.payload.WhichOneof("query")
            self._update_payload_proxy(self.default_query_type)
        else:
            self.default_query_type = queries[0][2]

        super().__init__(*args, **kwargs)

    @property
    def last_peer_address(self):
        # For "Execute @ <address>" button
        return self._application.last_chosen_peer

    def get_init_data(self):
        data = {
            **{
                field: str(self.query_proto_proxy.read(field))
                for field in self._plain_fields
            },
            ".payload.meta.query_counter": str(self._application.query_counter),
            "query_type": self.default_query_type,
        }
        if self.payload_proxy:
            for field in self.payload_proxy.descriptor:
                path = ".payload." + self.default_query_type + field["field_path"]
                value = self.payload_proxy.read(field["field_path"])
                logger.debug(value)
                logger.debug(type(value))
                if isinstance(value, int) or isinstance(value, str):
                    data[path] = str(value)
                else:
                    data[path] = value
        return data

    def update_data(self, frame_data):
        query_type = frame_data["query_type"]
        self._update_payload_proxy(query_type)

        self._update_proto_fields(frame_data)
        self._update_proto_status(frame_data)
        self._update_signature_status(frame_data)

        super().update_data(frame_data)

    def _update_payload_proxy(self, query_type):
        self.payload_proxy = ProtoMessageProxy(getattr(self.query.payload, query_type))

    def _update_proto_fields(self, frame_data):
        try:
            for field in frame_data:
                if field.startswith("."):  # considering all those protobuf fields
                    self.query_proto_proxy.set_to(field, frame_data[field])
            self.is_query_valid = True
        except Exception:
            self.is_query_valid = False

    def _update_proto_status(self, frame_data):
        frame_data["proto_status"] = {
            False: "<invalid protobuf data>",
            True: "<valid protobuf data>",
        }[self.is_query_valid]

    def _update_signature_status(self, frame_data):
        is_signature_valid = IrohaCrypto.is_signature_valid(
            self.query, self.query.signature
        )
        if is_signature_valid:
            frame_data["signature_status"] = "<valid> "
        else:
            frame_data["signature_status"] = "<invalid> "

        frame_data["signature_status"] += self.query.signature.signature

    def sign(self):
        self.go_to(
            SignaturePickerView,
            SignaturePickerModel,
            on_private_key_entered=self._sign_with_key,
        )

    def _sign_with_key(self, private_key):
        self.query = IrohaCrypto.sign_query(self.query, private_key)

    def save(self):
        if self.target_query:
            self.target_query.CopyFrom(self.query)
        else:
            self._application.queries.insert(0, self.query)

    def save_go_back(self):
        self.save()
        self.go_back()

    def execute(self):
        self.go_to(
            PeerPickerView, PeerPickerModel, on_peer_chosen=self._execute_with_address
        )

    def execute_at_last_peer(self):
        self._execute_with_address(self.last_peer_address)

    def _execute_with_address(self, address):
        self.go_to(GrpcRequestView, QuerySendModel, address=address, query=self.query)
