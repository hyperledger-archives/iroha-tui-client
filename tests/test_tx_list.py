from tests.framework import make_tui_instance


def test__simple():
    with make_tui_instance() as instance:
        instance.send("\r")
        instance.expect("Transaction Browser")


def create_simple_tx(instance):
    instance.expect("Transaction Editor")
    instance.send(
        ("tab", 3),  # Creator Account ID field
        "example@exampledomain",
        ("tab", 12),  # "Save & Go back" button
        "\r"
    )
    instance.expect("example@example")  # Clipped for 80x25 screens


def test__create__simple():
    with make_tui_instance() as instance:
        instance.send("\r")
        instance.expect("Transaction Browser")
        instance.send(
            ("tab", 3),
            "\r"
        )
        create_simple_tx(instance)


def test__edit__simple():
    with make_tui_instance() as instance:
        instance.send("\r")
        instance.expect("Transaction Browser")
        instance.send(
            ("tab", 3),
            "\r"
        )
        create_simple_tx(instance)
        instance.send(
            ("tab", 2),
            "\r",
            ("tab", 3),
            ("back", 100),
            "example2@exampledomain",
            ("tab", 12),
            "\r"
        )
