import os

from iroha_tui.models.base import BaseModel
from iroha_tui.tui.catch import catch
from iroha_tui.tui.popup import popup


class SaveFileModel(BaseModel):
    """
    Model for file save dialog.
    @param write_data - a function that gets called with the destination path when the user made their choice.
    @param default_file_path - a default value for the file path. Can be name only - then current dir is used.
    """

    def __init__(self, *args, **kwargs):
        self._write_data = kwargs.pop("write_data")
        self._init_data = {
            "file_path": kwargs.pop("default_file_path", "genesis_block.json")
        }
        super().__init__(*args, **kwargs)

    def get_init_data(self):
        return self._init_data

    @catch()
    def on_file_selected(self, path: str):
        def _popup(*args, **kwargs):
            popup(self._application.screen_manager, *args, **kwargs)

        def write():
            try:
                self._write_data(path)
                self.cancel()
                _popup(f"Successfully wrote the block to {path}.")
            except Exception as e:
                _popup(str(e))

        if not os.path.exists(path):
            write()
        else:

            def maybe_overwrite(answer):
                if answer == 0:
                    write()

            _popup(
                f"Name {path} already exists in the filesystem. Try to overwrite?",
                ["Yes", "No"],
                maybe_overwrite,
            )
