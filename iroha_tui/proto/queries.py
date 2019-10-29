from typing import List, Tuple

from iroha.queries_pb2 import Query
from iroha_tui.proto.helpers import add_spaces


# (human readable name, CamelCase name, snake_case name)
_QUERY_TUPLE = Tuple[str, str, str]


class ProtoQueryLoader:
    def __init__(self):
        self._queries = self._preload_queries()

    @property
    def queries(self):
        return self._queries

    def _preload_queries(self) -> List[_QUERY_TUPLE]:
        queries = []
        for query in Query.Payload.DESCRIPTOR.oneofs_by_name["query"].fields:
            query_name = query.message_type.name
            queries.append((add_spaces(query_name), query_name, query.name))
        return queries


class QueryWrapper:
    def __init__(self, unwrapped_query=None, wrapped_query=None):
        if not (bool(unwrapped_query) != bool(wrapped_query)):
            raise ValueError("Specify either wrapped or unwrapped query")

        self._wrapped = None
        self._unwrapped = None
        if unwrapped_query:
            self._init_from_unwrapped(unwrapped_query)
        else:
            self._init_from_wrapped(wrapped_query)

    @property
    def wrapped(self):
        return self._wrapped

    @property
    def unwrapped(self):
        return self._unwrapped

    def _init_from_unwrapped(self, unwrapped_query):
        queries = ProtoQueryLoader()
        name = unwrapped_query.DESCRIPTOR.name
        field_name = None
        for query in queries:
            if query[1] == name:
                field_name = query[2]
        proto_query = Query()
        target_query = getattr(proto_query.payload, field_name)
        target_query.CopyFrom(unwrapped_query)
        self._init_from_wrapped(proto_query)

    def _init_from_wrapped(self, wrapped_query):
        field_name = wrapped_query.payload.WhichOneof("query")
        self._wrapped = wrapped_query
        self._unwrapped = getattr(wrapped_query.payload, field_name)
