from iroha import IrohaCrypto
from iroha_tui.proto.helpers import add_spaces, capitalize_snake_case
from iroha_tui.proto.message import ProtoMessageProxy


class QueryViewer:
    def __init__(self, query):
        self._query = query
        self._data = self._precalc_data()

    @property
    def data(self):
        return self._data

    def _precalc_data(self):
        return {
            "creator": self._query.payload.meta.creator_account_id,
            "type": self._get_type(),
            "payload": self._get_payload(),
            "signature": self._get_signature_status()
        }

    def _get_type_field(self):
        return self._query.payload.WhichOneof("query")

    def _get_type(self):
        snake = self._get_type_field()
        capitalized = capitalize_snake_case(snake)
        return add_spaces(capitalized)

    def _get_payload(self):
        type_ = self._get_type_field()
        type_proxy = ProtoMessageProxy(getattr(self._query.payload, type_))
        payload_parts = []
        for field in type_proxy.descriptor:
            name = field["name"]
            path = field["field_path"]
            value = type_proxy.read(path)
            payload_parts.append(f"{name}={value}")
        return " ".join(payload_parts)

    def _get_signature_status(self):
        if not self._query.signature.signature:
            return " "
        if IrohaCrypto.is_signature_valid(self._query, self._query.signature):
            return "+"
        else:
            return "-"
