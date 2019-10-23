from functools import wraps

from torinaku.models.warning_popup import WarningModel
from torinaku.screens.warning_popup import WarningScreen


def catch(types=Exception):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except types as e:
                args[0].go_to(
                    WarningScreen,
                    WarningModel,
                    value=str(e)
                )
        return wrapped
    return wrapper
