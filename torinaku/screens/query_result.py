from torinaku.screens.base import BaseScreen
from torinaku.tui.layout_composers.proto import ProtoLayoutComposer


class QueryResultView(BaseScreen):
    def _compose_layout(self):
        ProtoLayoutComposer.compose_on_frame(self, self._model.result_proxy)
