from tests.framework import make_tui_instance


def test__command__add():
    with make_tui_instance() as instance:
        instance.send(
            "\r",
            "tab",
            "\r",
            ("tab", 7),
            "\r"
        )
        instance.expect("Add command")
        instance.send(
            "down",
            "\r"
        )
        instance.expect("Command Editor")
        instance.expect("Add Peer")
        instance.send(
            ("tab", 2),
            "127.0.0.1:50051",
            "tab",
            "example_key",
            "tab",
            "\r"
        )
        instance.expect("AddPeer")


def test__command__edit():
    with make_tui_instance() as instance:
        instance.send(
            "\r",
            "tab",
            "\r",
            ("tab", 7),
            "\r"
        )
        instance.expect("Command Editor")
        instance.send(
            ("tab", 3),
            ("back", 100),
            "exkey",
            ("tab", 2),
            "\r"
        )
        instance.expect("exkey")
