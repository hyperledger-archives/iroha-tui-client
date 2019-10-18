from tests.framework import AppInstance


class TorinakuInstance:
    def __init__(self):
        self.child: AppInstance = None

    def __enter__(self):
        self.child = AppInstance("python3 -m torinaku")
        return self.child

    def __exit__(self, *args, **kwargs):
        self.child.close()
