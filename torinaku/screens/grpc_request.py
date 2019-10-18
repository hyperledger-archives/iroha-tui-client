from asciimatics.widgets import Layout, TextBox, Button, Divider

from torinaku.screens.base import BaseScreen


class GrpcRequestView(BaseScreen):
    _title = "gRPC request"

    def __init__(self, *args, **kwargs):
        self._log = None
        super().__init__(*args, **kwargs)

    def update(self, frame_no):
        self._log.value = self._model.log
        self._proceed_button.disabled = not self._model.is_proceed_available
        self._retry_button.disabled = not self._model.is_request_completed
        self._cancel_button.disabled = not self._model.is_request_completed
        super().update(frame_no)

    def _compose_layout(self):
        log_layout = Layout([1])
        self.add_layout(log_layout)
        self._log = TextBox(
            height=self._canvas.height - 4, disabled=True, line_wrap=True
        )
        log_layout.add_widget(self._log)
        log_layout.add_widget(Divider())

        actions_layout = Layout([1, 1, 1])
        self.add_layout(actions_layout)
        self._proceed_button = Button(
            text=self._model.proceed_caption,
            on_click=self._model.proceed,
            disabled=True,
        )
        actions_layout.add_widget(self._proceed_button, 0)
        self._retry_button = Button(
            text="Retry", on_click=self._model.retry, disabled=True
        )
        actions_layout.add_widget(self._retry_button, 1)
        self._cancel_button = Button(text="Cancel", on_click=self._model.cancel)
        actions_layout.add_widget(self._cancel_button, 2)
