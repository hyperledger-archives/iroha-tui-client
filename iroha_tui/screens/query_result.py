from iroha_tui.screens.base import BaseScreen
from iroha_tui.tui.layout_composers.proto import ProtoLayoutComposer


class QueryResultView(BaseScreen):
    def _compose_layout(self):
        ProtoLayoutComposer.compose_on_frame(self, self._model.result_proxy)
